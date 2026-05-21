from derivacion_drm.domain.word_spec import (
    ParagraphSpec, RunSpec, TableSpec, WordDocumentSpec,
)


def test_run_spec_defaults_plain():
    r = RunSpec(text="hola")
    assert r.bold is False and r.underline is False and r.uppercase is False
    assert r.hyperlink is None


def test_paragraph_spec_default_line_spacing_115():
    p = ParagraphSpec(runs=[RunSpec(text="x")])
    assert p.line_spacing == 1.15
    assert p.alignment == "left"
    assert p.indent_first_line_cm is None


def test_word_document_spec_defaults():
    s = WordDocumentSpec(paragraphs=[], filename="x.docx", incluir_logo=False)
    assert "Pedro De Valdivia" in s.footer_text


def test_table_spec_default_style():
    t = TableSpec(rows=[("A", "1"), ("B", "2")])
    assert t.style == "Table Grid"
