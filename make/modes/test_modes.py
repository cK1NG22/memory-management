#!/usr/bin/env python3
"""Tests for modes.py. Run: python3 make/modes/test_modes.py

Every test builds a throwaway project and library, so nothing here reads or
writes the real library or any real project.
"""
import contextlib, io, os, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import modes

REAL = Path(__file__).resolve().parent


def quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return fn(*a, **k)


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name).resolve()
        self.project = root / "proj"
        self.library = root / "library"
        self.templates = root / "templates"
        for m in modes.MODES:
            (self.library / m / "rules").mkdir(parents=True)
            (self.library / m / "rules" / f"{m}.md").write_text(f"# {m} rule\n")
            (self.templates / m).mkdir(parents=True)
            (self.templates / m / "CLAUDE.md").write_text(f"# Mode: {m}\n\n{modes.POINTER}")
        (self.templates / "CLAUDE.md").write_text("# {{PROJECT}}\n\nmade {{DATE}}\n")
        self.project.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def stamp(self, **k):
        return quiet(modes.stamp, self.project, self.library, self.templates, **k)

    def rule(self, m):
        return self.project / m / ".claude" / "rules" / f"{m}.md"


class Stamp(Base):
    def test_fresh_project_is_clean(self):
        self.assertEqual(self.stamp(), 0)
        for m in modes.MODES:
            self.assertTrue(self.rule(m).is_file())
            self.assertFalse(self.rule(m).is_symlink())
        self.assertIn("# proj", (self.project / "CLAUDE.md").read_text())
        self.assertEqual(modes.check(self.project, self.library), [])

    def test_dry_run_writes_nothing(self):
        self.assertEqual(self.stamp(dry=True), 0)
        self.assertEqual(list(self.project.iterdir()), [])

    def test_rerun_keeps_existing_files(self):
        self.stamp()
        (self.project / "CLAUDE.md").write_text("mine\n")
        self.assertEqual(self.stamp(), 0)
        self.assertEqual((self.project / "CLAUDE.md").read_text(), "mine\n")

    def test_edited_copy_is_reported_then_updated(self):
        self.stamp()
        self.rule("plan").write_text("edited here\n")
        self.assertEqual(self.stamp(), 1)                       # reported, not overwritten
        self.assertEqual(self.rule("plan").read_text(), "edited here\n")
        self.assertEqual(self.stamp(update=True), 0)
        self.assertEqual(self.rule("plan").read_text(), "# plan rule\n")

    def test_local_rule_is_left_alone(self):
        self.stamp()
        local = self.rule("make").with_name("house.md")
        local.write_text("project-only rule\n")
        self.assertEqual(self.stamp(update=True), 0)
        self.assertEqual(local.read_text(), "project-only rule\n")

    def test_symlinked_rule_becomes_a_real_copy(self):
        self.rule("make").parent.mkdir(parents=True)
        os.symlink(self.library / "make" / "rules" / "make.md", self.rule("make"))
        self.assertEqual(self.stamp(), 0)
        self.assertFalse(self.rule("make").is_symlink())

    def test_old_wiring_is_removed(self):
        for m in modes.MODES:
            up = m.upper()
            (self.project / m).mkdir()
            os.symlink(self.library / m / "rules" / f"{m}.md", self.project / m / f"{up}-MODE.md")
            (self.project / m / "CLAUDE.md").write_text(
                f"# Mode: {m}\n\nkeep this line\n\n## Mode principles (single source: x)\n\n@{up}-MODE.md\n")
        self.assertEqual(self.stamp(), 0)
        for m in modes.MODES:
            text = (self.project / m / "CLAUDE.md").read_text()
            self.assertNotIn("-MODE.md", text)
            self.assertIn("keep this line", text)
            self.assertEqual(text.count("## Mode principles"), 1)
            self.assertFalse((self.project / m / f"{m.upper()}-MODE.md").is_symlink())

    def test_empty_library_refuses(self):
        (self.library / "plan" / "rules" / "plan.md").unlink()
        self.assertEqual(self.stamp(), 2)
        self.assertEqual(list(self.project.iterdir()), [])


class Check(Base):
    """Negative tests: each proves the check can fail."""

    def setUp(self):
        super().setUp()
        self.stamp()

    def problems(self):
        return modes.check(self.project, self.library)

    def test_missing_rule(self):
        self.rule("research").unlink()
        self.assertTrue(any("missing" in p for p in self.problems()))

    def test_drifted_rule(self):
        self.rule("research").write_text("drift\n")
        self.assertTrue(any("differs" in p for p in self.problems()))

    def test_symlinked_rule(self):
        self.rule("make").unlink()
        os.symlink(self.library / "make" / "rules" / "make.md", self.rule("make"))
        self.assertTrue(any("symlink" in p for p in self.problems()))

    def test_symlinked_rules_folder(self):
        rules = self.rule("make").parent
        self.rule("make").unlink()
        rules.rmdir()
        os.symlink(self.library / "make" / "rules", rules)
        self.assertTrue(any("through a symlink" in p for p in self.problems()))

    def test_dead_skill_link(self):
        d = self.project / "plan" / ".claude" / "skills"
        d.mkdir(parents=True)
        os.symlink(self.project / "nowhere", d / "ghost")
        self.assertTrue(any("dead symlink" in p for p in self.problems()))

    def test_leftover_import(self):
        md = self.project / "plan" / "CLAUDE.md"
        md.write_text(md.read_text() + "\n@PLAN-MODE.md\n")
        self.assertTrue(any("still imports" in p for p in self.problems()))

    def test_missing_mode_folder(self):
        import shutil
        shutil.rmtree(self.project / "research")
        self.assertTrue(any("research/ folder is missing" in p for p in self.problems()))


class Place(Base):
    def setUp(self):
        super().setUp()
        self.stamp()
        self.dot = self.project / ".claude"
        (self.dot / "skills" / "probe").mkdir(parents=True)
        (self.dot / "skills" / "probe" / "SKILL.md").write_text("---\ndescription: a probe\n---\n")
        (self.dot / "agents").mkdir()
        (self.dot / "agents" / "grader.md").write_text("---\ndescription: grades\n---\n")
        (self.dot / "rules").mkdir()
        (self.dot / "rules" / "style.md").write_text("style\n")
        self.outside = Path(self.tmp.name).resolve() / "global"
        (self.outside / "skills" / "shared").mkdir(parents=True)
        (self.outside / "skills" / "shared" / "SKILL.md").write_text("---\ndescription: s\n---\n")
        (self.outside / "rules").mkdir()
        (self.outside / "rules" / "law.md").write_text("law\n")

    def place(self, *a, **k):
        return quiet(modes.place, self.project, *a, **k)

    def test_in_project_item_moves(self):
        self.assertEqual(self.place("skills", "probe", "make"), 0)
        self.assertFalse((self.dot / "skills" / "probe").exists())
        self.assertTrue((self.project / "make/.claude/skills/probe/SKILL.md").is_file())
        self.assertEqual(self.place("agents", "grader", "research"), 0)
        self.assertTrue((self.project / "research/.claude/agents/grader.md").is_file())
        self.assertEqual(self.place("rules", "style", "plan"), 0)
        self.assertTrue((self.project / "plan/.claude/rules/style.md").is_file())

    def test_outside_skill_links_and_rule_copies(self):
        self.assertEqual(self.place("skills", "shared", "plan", source_dot=self.outside), 0)
        dst = self.project / "plan/.claude/skills/shared"
        self.assertTrue(dst.is_symlink() and dst.exists())
        self.assertTrue((self.outside / "skills" / "shared").exists())     # source untouched
        self.assertEqual(self.place("rules", "law", "make", source_dot=self.outside), 0)
        dst = self.project / "make/.claude/rules/law.md"
        self.assertTrue(dst.is_file() and not dst.is_symlink())

    def test_linking_a_rule_is_refused(self):
        self.assertEqual(self.place("rules", "law", "make", source_dot=self.outside, how="link"), 2)
        self.assertFalse((self.project / "make/.claude/rules/law.md").exists())

    def test_existing_destination_is_refused(self):
        self.place("skills", "shared", "plan", source_dot=self.outside)
        self.assertEqual(self.place("skills", "shared", "plan", source_dot=self.outside), 2)

    def test_moving_a_relative_link_keeps_it_resolving(self):
        os.symlink("../../../global/skills/shared", self.dot / "skills" / "rel")
        self.assertTrue((self.dot / "skills" / "rel").exists())
        self.assertEqual(self.place("skills", "rel", "research"), 0)
        self.assertTrue((self.project / "research/.claude/skills/rel/SKILL.md").is_file())
        self.assertFalse((self.dot / "skills" / "rel").is_symlink())

    def test_dry_run_moves_nothing(self):
        self.assertEqual(self.place("skills", "probe", "make", dry=True), 0)
        self.assertTrue((self.dot / "skills" / "probe").exists())

    def test_unknown_item(self):
        self.assertEqual(self.place("skills", "nope", "make"), 2)

    def test_back_to_root(self):
        self.place("skills", "probe", "make")
        self.assertEqual(self.place("skills", "probe", "root",
                                    source_dot=self.project / "make" / ".claude"), 0)
        self.assertTrue((self.dot / "skills" / "probe" / "SKILL.md").is_file())

    def test_listing_runs(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            modes.listing(self.project, self.outside)
        out = buf.getvalue()
        for word in ("probe", "grader", "style.md", "shared", "a probe"):
            self.assertIn(word, out)


class Shipped(unittest.TestCase):
    """The real library and templates this skill ships with."""

    def test_real_library_and_templates_stamp_clean(self):
        with tempfile.TemporaryDirectory() as t:
            project = Path(t).resolve() / "demo"
            project.mkdir()
            rc = quiet(modes.stamp, project, REAL / "library", REAL / "templates")
            self.assertEqual(rc, 0)
            for m in modes.MODES:
                self.assertNotIn("-MODE.md", (project / m / "CLAUDE.md").read_text())
            self.assertNotIn("{{", (project / "CLAUDE.md").read_text())


if __name__ == "__main__":
    unittest.main()
