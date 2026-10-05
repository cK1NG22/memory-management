#!/usr/bin/env python3
"""Mode folders for a project: stamp them, sort things into them, check them.

  modes.py stamp [DIR] [--dry-run] [--update]   create research/ plan/ make/ and copy library rules
  modes.py check DIR [DIR...]                   report anything that silently fails to load
  modes.py list  [DIR] [--from DIR]             inventory skills, agents and rules, by where they load
  modes.py place KIND NAME MODE [--project DIR] [--from DIR] [--move|--link|--copy] [--dry-run]

The loading facts this rides on (probed 2026-09-28 on CLI 2.1.284, re-probed
2026-10-04 on 2.1.289 — re-test after CLI upgrades):

  - <project>/<mode>/.claude/{rules,skills,agents}/ load ONLY when the session
    starts in <mode>/. A session at the project root sees none of them.
  - Rules skip symlinks: a symlinked rule file or folder silently never loads.
    So mode rules are real copies of the library files, and `check` exists to
    catch the copies drifting apart.
  - Skills and agents follow symlinks, so those are linked, not copied. A dead
    link vanishes with no warning, which `check` also catches.

A project rule with the same filename as a library rule is that rule's copy.
Any other filename is a project-local rule and is never touched or compared.
"""
import argparse, datetime, filecmp, os, re, shutil, subprocess, sys
from pathlib import Path

MODES = ("research", "plan", "make")
KINDS = ("rules", "skills", "agents")
HERE = Path(__file__).resolve().parent      # resolve(): the skill may be reached through a symlink

POINTER = """## Mode principles

The rule files in `.claude/rules/` beside this file. They load when a session starts in this folder.
They are copies from the mode library; `modes.py check` reports any that differ.
"""


def say(tag, msg):
    print(f"  {tag:<8}{msg}")


def library_rules(library, mode):
    return sorted((library / mode / "rules").glob("*.md"))


def legacy_import(mode):
    return f"@{mode.upper()}-MODE.md"


# ── stamp ────────────────────────────────────────────────────────────────────

def stamp_templates(project, templates, dry):
    tokens = {"{{PROJECT}}": project.name, "{{DATE}}": datetime.date.today().isoformat()}
    for src in sorted(p for p in templates.rglob("*") if p.is_file()):
        rel = src.relative_to(templates)
        dst = project / rel
        if dst.exists() or dst.is_symlink():
            say("keep", rel)
            continue
        say("create", rel)
        if not dry:
            text = src.read_text()
            for k, v in tokens.items():
                text = text.replace(k, v)
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(text)


def stamp_rules(project, library, dry, update):
    for mode in MODES:
        for src in library_rules(library, mode):
            dst = project / mode / ".claude" / "rules" / src.name
            rel = dst.relative_to(project)
            if dst.is_symlink():
                # a symlinked rule never loads; a real copy is the fix
                say("replace", f"{rel} (was a symlink, which never loads)")
            elif not dst.exists():
                say("copy", rel)
            elif filecmp.cmp(src, dst, shallow=False):
                say("keep", rel)
                continue
            elif update:
                say("update", rel)
            else:
                say("DIFFERS", f"{rel} differs from the library (--update overwrites it)")
                continue
            if not dry:
                dst.parent.mkdir(parents=True, exist_ok=True)
                if dst.is_symlink():
                    dst.unlink()
                shutil.copyfile(src, dst)


def remove_legacy(project, dry):
    """The previous wiring: <mode>/<MODE>-MODE.md symlink + an @import line.
    Both go, or the project carries two copies of the same principles."""
    for mode in MODES:
        link = project / mode / f"{mode.upper()}-MODE.md"
        if link.is_symlink():
            say("remove", f"{link.relative_to(project)} (old symlink)")
            if not dry:
                link.unlink()
        elif link.exists():
            say("SKIP", f"{link.relative_to(project)} is a regular file — move its content into "
                        f"{mode}/.claude/rules/ by hand")

        md = project / mode / "CLAUDE.md"
        if not md.is_file():
            continue
        lines = md.read_text().splitlines()
        hits = [i for i, l in enumerate(lines) if l.strip() == legacy_import(mode)]
        if not hits:
            continue
        say("edit", f"{md.relative_to(project)} (drop {legacy_import(mode)})")
        i = hits[0]
        start = i
        j = i - 1
        while j >= 0 and not lines[j].strip():
            j -= 1
        if j >= 0 and lines[j].startswith("## Mode principles"):
            start = j
        new = lines[:start] + POINTER.rstrip("\n").splitlines() + lines[i + 1:]
        if not dry:
            md.write_text("\n".join(new).rstrip("\n") + "\n")


def in_git_repo(project):
    try:
        r = subprocess.run(["git", "-C", str(project), "rev-parse", "--git-dir"],
                           capture_output=True)
        return r.returncode == 0
    except OSError:
        return False


def stamp(project, library, templates, dry=False, update=False):
    print(f"Stamping mode folders onto {project}" + ("  [dry-run]" if dry else ""))
    missing = [m for m in MODES if not library_rules(library, m)]
    if missing:
        print(f"error: the library at {library} has no rules for: {', '.join(missing)}",
              file=sys.stderr)
        return 2
    stamp_templates(project, templates, dry)
    stamp_rules(project, library, dry, update)
    remove_legacy(project, dry)
    if dry:
        print("\nNothing was changed. Re-run without --dry-run to apply.")
        return 0
    problems = check(project, library)
    report(project, problems)
    return 1 if problems else 0


# ── check ────────────────────────────────────────────────────────────────────

def check(project, library):
    """Everything here fails with no warning inside a session, so it is checked
    from outside one. Returns a list of problem strings (empty = clean)."""
    bad = []
    for mode in MODES:
        mdir = project / mode
        if not mdir.is_dir():
            bad.append(f"{mode}/ folder is missing")
            continue
        if not (mdir / "CLAUDE.md").is_file():
            bad.append(f"{mode}/CLAUDE.md is missing")
        elif legacy_import(mode) in (mdir / "CLAUDE.md").read_text().split():
            bad.append(f"{mode}/CLAUDE.md still imports {legacy_import(mode)}")
        if (mdir / f"{mode.upper()}-MODE.md").is_symlink():
            bad.append(f"{mode}/{mode.upper()}-MODE.md old symlink is still there")

        dot = mdir / ".claude"
        rules = dot / "rules"
        if dot.is_symlink() or rules.is_symlink():
            bad.append(f"{mode}/.claude/rules is reached through a symlink — rules never load")
        elif rules.is_dir():
            for f in sorted(rules.rglob("*")):
                if f.is_symlink():
                    bad.append(f"{f.relative_to(project)} is a symlink — it never loads")
        for src in library_rules(library, mode):
            dst = rules / src.name
            if dst.is_symlink():
                continue                               # already reported above
            if not dst.is_file():
                bad.append(f"{dst.relative_to(project)} is missing (library has it)")
            elif not filecmp.cmp(src, dst, shallow=False):
                bad.append(f"{dst.relative_to(project)} differs from the library")

        for kind in ("skills", "agents"):
            d = dot / kind
            if d.is_symlink() and not d.exists():
                bad.append(f"{mode}/.claude/{kind} is a dead symlink — everything in it vanished")
            elif d.is_dir():
                for e in sorted(d.iterdir()):
                    if e.is_symlink() and not e.exists():
                        bad.append(f"{e.relative_to(project)} is a dead symlink -> {os.readlink(e)}")
    return bad


def report(project, problems):
    if problems:
        print(f"\n❌ {project}: {len(problems)} problem(s)")
        for p in problems:
            print(f"   {p}")
    else:
        print(f"\n✅ {project}: mode folders are sound — rules are real files and match the library.")
    if not in_git_repo(project):
        print("   note: not a git repo. Native memory keys to the git root; without one, each mode\n"
              "   folder gets its own separate store. Run `git init` before the first session.")


# ── list ─────────────────────────────────────────────────────────────────────

def describe(path):
    """First `description:` in the frontmatter, for a skill folder or an .md file."""
    f = path / "SKILL.md" if path.is_dir() else path
    try:
        text = f.read_text(errors="ignore")
    except OSError:
        return ""
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    if m:
        d = re.search(r"^description:\s*(.+)$", m.group(1), re.M)
        if d:
            return d.group(1).strip().strip("\"'")
    for line in text.splitlines():                      # no frontmatter: first heading or line
        if line.strip() and line.strip() != "---":
            return line.strip().lstrip("# ")
    return ""


def items(dot, kind):
    """Skills are folders holding SKILL.md; agents and rules are .md files."""
    d = dot / kind
    if not d.is_dir():
        return []
    if kind == "skills":
        return sorted(e for e in d.iterdir() if (e / "SKILL.md").exists() or e.is_symlink())
    if kind == "rules":
        return sorted(e for e in d.rglob("*.md") if "_archive" not in e.parts)
    return sorted(e for e in d.glob("*.md"))


def size(path):
    f = path / "SKILL.md" if path.is_dir() else path
    try:
        return f.stat().st_size
    except OSError:
        return 0


def listing(project, extra):
    places = [("root", project / ".claude")] + [(m, project / m / ".claude") for m in MODES]
    if extra:
        places.append((f"from:{extra}", extra))
    rows = []
    for where, dot in places:
        for kind in KINDS:
            for e in items(dot, kind):
                name = e.name if kind == "skills" else str(e.relative_to(dot / kind))
                note = ""
                if e.is_symlink():
                    note = " [link]" if e.exists() else " [DEAD LINK]"
                rows.append((where, kind, name + note, size(e), describe(e)[:70]))
    if not rows:
        print("Nothing found.")
        return 0
    w = [max(len(str(r[i])) for r in rows) for i in range(3)]
    print(f"{'loads in':<{w[0]}}  {'kind':<{w[1]}}  {'name':<{w[2]}}  {'chars':>6}  description")
    for r in rows:
        print(f"{r[0]:<{w[0]}}  {r[1]:<{w[1]}}  {r[2]:<{w[2]}}  {r[3]:>6}  {r[4]}")
    print("\n'root' loads in every session in the project; a mode loads only when the session "
          "starts in that folder; 'from:' rows load nowhere in this project yet.")
    return 0


# ── place ────────────────────────────────────────────────────────────────────

def find_source(dot, kind, name):
    base = dot / kind
    for cand in (base / name, base / f"{name}.md"):
        if cand.exists() or cand.is_symlink():
            return cand
    return None


def place(project, kind, name, mode, source_dot=None, how=None, dry=False):
    dot = source_dot if source_dot is not None else project / ".claude"
    src = find_source(dot, kind, name)
    if src is None:
        print(f"error: no {kind[:-1]} named {name!r} in {dot / kind}", file=sys.stderr)
        return 2
    if not src.exists():
        print(f"error: {src} is a dead symlink -> {os.readlink(src)}", file=sys.stderr)
        return 2
    dst_dot = project / ".claude" if mode == "root" else project / mode / ".claude"
    dst = dst_dot / kind / src.name
    if dst.exists() or dst.is_symlink():
        print(f"error: {dst} already exists", file=sys.stderr)
        return 2

    home = src.parent.resolve()                        # where the entry itself sits, not its target
    inside = project.resolve() == home or project.resolve() in home.parents
    if how is None:
        how = "move" if inside else ("copy" if kind == "rules" else "link")
    if kind == "rules" and how == "link":
        print("error: rules skip symlinks — a linked rule never loads. Use --copy.", file=sys.stderr)
        return 2
    if kind == "rules" and how == "move" and src.is_symlink():
        how = "copy"                                   # never carry a rule symlink forward

    say(how, f"{src}  ->  {dst}")
    if dry:
        return 0
    dst.parent.mkdir(parents=True, exist_ok=True)
    target = src.resolve()
    if how == "link":
        os.symlink(target, dst)
    elif how == "copy":
        if target.is_dir():
            shutil.copytree(target, dst)
        else:
            shutil.copyfile(target, dst)
    elif src.is_symlink():
        # moving a link: re-point it at the absolute target, or a relative link breaks
        os.symlink(target, dst)
        src.unlink()
    else:
        shutil.move(str(src), str(dst))
    if not dst.exists():
        print(f"error: {dst} does not resolve after the {how}", file=sys.stderr)
        return 1
    if how == "move" and mode != "root":
        say("note", f"{src.name} now loads only in sessions started in {mode}/")
    return 0


# ── cli ──────────────────────────────────────────────────────────────────────

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("stamp", help="create mode folders and copy library rules")
    s.add_argument("dir", nargs="?", default=".")
    s.add_argument("--dry-run", action="store_true")
    s.add_argument("--update", action="store_true", help="overwrite rule copies that differ")
    s.add_argument("--library")
    s.add_argument("--templates")

    c = sub.add_parser("check", help="report anything that silently fails to load")
    c.add_argument("dirs", nargs="+")
    c.add_argument("--library")

    l = sub.add_parser("list", help="inventory skills, agents and rules")
    l.add_argument("dir", nargs="?", default=".")
    l.add_argument("--from", dest="source", help="another .claude folder to list as candidates")

    p = sub.add_parser("place", help="move, link or copy one item into a mode folder")
    p.add_argument("kind", choices=KINDS)
    p.add_argument("name")
    p.add_argument("mode", choices=MODES + ("root",))
    p.add_argument("--project", default=".")
    p.add_argument("--from", dest="source", help="the .claude folder holding the item")
    how = p.add_mutually_exclusive_group()
    for h in ("move", "link", "copy"):
        how.add_argument(f"--{h}", dest="how", action="store_const", const=h)
    p.add_argument("--dry-run", action="store_true")

    a = ap.parse_args(argv)
    path = lambda v: Path(v).expanduser().resolve()
    library = path(a.library) if getattr(a, "library", None) else HERE / "library"

    if a.cmd == "stamp":
        project = path(a.dir)
        if not a.dry_run:
            project.mkdir(parents=True, exist_ok=True)
        templates = path(a.templates) if a.templates else HERE / "templates"
        return stamp(project, library, templates, a.dry_run, a.update)
    if a.cmd == "check":
        worst = 0
        for d in a.dirs:
            problems = check(path(d), library)
            report(path(d), problems)
            worst = max(worst, 1 if problems else 0)
        return worst
    if a.cmd == "list":
        return listing(path(a.dir), Path(a.source).expanduser() if a.source else None)
    if a.cmd == "place":
        return place(path(a.project), a.kind, a.name, a.mode,
                     Path(a.source).expanduser() if a.source else None, a.how, a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
