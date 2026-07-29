import unittest

from mdextractor import (
    markdown_to_blocks,
    markdown_to_html_root_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestMDExtractor(unittest.TestCase):
    def test_split_nodes_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE_TEXT)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN_TEXT)

    def test_split_nodes_no_delimiter(self):
        node = TextNode("This is text with no delimiter", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is text with no delimiter")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)

    def test_split_nodes_multiple_delimiters(self):
        node = TextNode(
            "This is text with multiple `code block` words `in it`", TextType.PLAIN_TEXT
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with multiple ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE_TEXT)
        self.assertEqual(new_nodes[2].text, " words ")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[3].text, "in it")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE_TEXT)

    def test_split_nodes_bold_delimiter(self):
        node = TextNode(
            "This is text with multiple **bold** words **in it**", TextType.PLAIN_TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with multiple ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD_TEXT)
        self.assertEqual(new_nodes[2].text, " words ")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[3].text, "in it")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD_TEXT)

    def test_split_nodes_non_text_node(self):
        node = TextNode("This is a bold text node", TextType.BOLD_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is a bold text node")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD_TEXT)

    def test_split_nodes_multiple_old_nodes(self):
        node1 = TextNode("This is a **bold1** text node", TextType.PLAIN_TEXT)
        node2 = TextNode("This is a **bold2** text node", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD_TEXT)
        self.assertEqual(len(new_nodes), 6)
        self.assertEqual(new_nodes[0].text, "This is a ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[1].text, "bold1")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD_TEXT)
        self.assertEqual(new_nodes[2].text, " text node")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[3].text, "This is a ")
        self.assertEqual(new_nodes[3].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(new_nodes[4].text, "bold2")
        self.assertEqual(new_nodes[4].text_type, TextType.BOLD_TEXT)
        self.assertEqual(new_nodes[5].text, " text node")
        self.assertEqual(new_nodes[5].text_type, TextType.PLAIN_TEXT)

    def test_split_nodes_no_match_delimiters(self):
        node = TextNode(
            "This is text with no `matching delimiters", TextType.PLAIN_TEXT
        )
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "![one](https://example.com/1.png) and ![two](https://example.com/2.png)"
        )
        self.assertListEqual(
            [
                ("one", "https://example.com/1.png"),
                ("two", "https://example.com/2.png"),
            ],
            matches,
        )

    def test_extract_markdown_images_false_ones(self):
        matches = extract_markdown_images(
            "Not an image: [image](https://example.com/1.png) and ![broken](missing"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "[one](https://example.com/1) and [two](https://example.com/2)"
        )
        self.assertListEqual(
            [("one", "https://example.com/1"), ("two", "https://example.com/2")],
            matches,
        )

    def test_extract_markdown_links_false_ones(self):
        matches = extract_markdown_links(
            "Not a link: (https://example.com) and [broken](missing"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_tricky_mixed_text(self):
        text = (
            "Start ![img](https://example.com/img.png) mid [link](https://example.com) "
            "end ![alt text](https://example.com/a-b_c.png) and [another](https://example.com?q=1)"
        )
        self.assertListEqual(
            [
                ("img", "https://example.com/img.png"),
                ("alt text", "https://example.com/a-b_c.png"),
            ],
            extract_markdown_images(text),
        )
        self.assertListEqual(
            [
                ("link", "https://example.com"),
                ("another", "https://example.com?q=1"),
            ],
            extract_markdown_links(text),
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_empty_text(self):
        node = TextNode("", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("", TextType.PLAIN_TEXT)], new_nodes)

    def test_split_images_no_images(self):
        node = TextNode("This is just plain text with no images", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is just plain text with no images", TextType.PLAIN_TEXT)],
            new_nodes,
        )

    def test_split_images_image_at_start(self):
        node = TextNode(
            "![start](https://example.com/start.png) followed by text",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "https://example.com/start.png"),
                TextNode(" followed by text", TextType.PLAIN_TEXT),
            ],
            new_nodes,
        )

    def test_split_images_image_at_end(self):
        node = TextNode(
            "Text followed by ![end](https://example.com/end.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text followed by ", TextType.PLAIN_TEXT),
                TextNode("end", TextType.IMAGE, "https://example.com/end.png"),
            ],
            new_nodes,
        )

    def test_split_images_consecutive_images(self):
        node = TextNode(
            "![first](https://example.com/1.png)![second](https://example.com/2.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "https://example.com/1.png"),
                TextNode("second", TextType.IMAGE, "https://example.com/2.png"),
            ],
            new_nodes,
        )

    def test_split_links_empty_text(self):
        node = TextNode("", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("", TextType.PLAIN_TEXT)], new_nodes)

    def test_split_links_no_links(self):
        node = TextNode("This is just plain text with no links", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is just plain text with no links", TextType.PLAIN_TEXT)],
            new_nodes,
        )

    def test_split_links_link_at_start(self):
        node = TextNode(
            "[start](https://example.com/start) followed by text",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.LINK, "https://example.com/start"),
                TextNode(" followed by text", TextType.PLAIN_TEXT),
            ],
            new_nodes,
        )

    def test_split_links_link_at_end(self):
        node = TextNode(
            "Text followed by [end](https://example.com/end)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text followed by ", TextType.PLAIN_TEXT),
                TextNode("end", TextType.LINK, "https://example.com/end"),
            ],
            new_nodes,
        )

    def test_split_links_consecutive_links(self):
        node = TextNode(
            "[first](https://example.com/1)[second](https://example.com/2)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.LINK, "https://example.com/1"),
                TextNode("second", TextType.LINK, "https://example.com/2"),
            ],
            new_nodes,
        )

    def test_split_images_mixed_with_false_markup(self):
        node = TextNode(
            "This has ![real](https://example.com/real.png) and [not-an-image](url) text",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This has ", TextType.PLAIN_TEXT),
                TextNode("real", TextType.IMAGE, "https://example.com/real.png"),
                TextNode(" and [not-an-image](url) text", TextType.PLAIN_TEXT),
            ],
            new_nodes,
        )

    def test_split_links_mixed_with_false_markup(self):
        node = TextNode(
            "This has [real](https://example.com) and ![not-a-link](url) text",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This has ", TextType.PLAIN_TEXT),
                TextNode("real", TextType.LINK, "https://example.com"),
                TextNode(" and ![not-a-link](url) text", TextType.PLAIN_TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        result = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN_TEXT),
                TextNode("text", TextType.BOLD_TEXT),
                TextNode(" with an ", TextType.PLAIN_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" word and a ", TextType.PLAIN_TEXT),
                TextNode("code block", TextType.CODE_TEXT),
                TextNode(" and an ", TextType.PLAIN_TEXT),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.PLAIN_TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            result,
        )

    def test_text_to_textnodes_plain_text(self):
        result = text_to_textnodes("This is just plain text")
        self.assertListEqual(
            [TextNode("This is just plain text", TextType.PLAIN_TEXT)],
            result,
        )

    def test_text_to_textnodes_bold_only(self):
        result = text_to_textnodes("**bold text**")
        self.assertListEqual(
            [TextNode("bold text", TextType.BOLD_TEXT)],
            result,
        )

    def test_text_to_textnodes_italic_only(self):
        result = text_to_textnodes("_italic text_")
        self.assertListEqual(
            [TextNode("italic text", TextType.ITALIC_TEXT)],
            result,
        )

    def test_text_to_textnodes_code_only(self):
        result = text_to_textnodes("`code text`")
        self.assertListEqual(
            [TextNode("code text", TextType.CODE_TEXT)],
            result,
        )

    def test_text_to_textnodes_link_only(self):
        result = text_to_textnodes("[link text](https://example.com)")
        self.assertListEqual(
            [TextNode("link text", TextType.LINK, "https://example.com")],
            result,
        )

    def test_text_to_textnodes_image_only(self):
        result = text_to_textnodes("![alt text](https://example.com/image.png)")
        self.assertListEqual(
            [TextNode("alt text", TextType.IMAGE, "https://example.com/image.png")],
            result,
        )

    def test_text_to_textnodes_mixed_formatting(self):
        result = text_to_textnodes("_italic_ and **bold** and `code`")
        self.assertListEqual(
            [
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode("bold", TextType.BOLD_TEXT),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode("code", TextType.CODE_TEXT),
            ],
            result,
        )

    def test_text_to_textnodes_empty_string(self):
        result = text_to_textnodes("")
        self.assertListEqual([], result)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_blank_lines(self):
        md = """

First block



Second block


Third block

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block",
                "Second block",
                "Third block",
            ],
        )

    def test_markdown_to_blocks_trims_block_whitespace(self):
        md = """
   First block with spaces   

    Second block line one    
Second block line two   
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block with spaces",
                "Second block line one    \nSecond block line two",
            ],
        )

    def test_markdown_to_blocks_whitespace_only(self):
        md = "\n   \n\t\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""

        root_node = markdown_to_html_root_node(md)
        html = root_node.to_html()
        self.assertEqual(
            html,
            "<html><head></head><body><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></body></html>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        root_node = markdown_to_html_root_node(md)
        html = root_node.to_html()
        self.assertEqual(
            html,
            "<html><head></head><body><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></body></html>",
        )

    def test_codeblock_with_backticks(self):
        md = """
```
This has `backticks` inside
and **bold** should _not_ parse
```
"""

        root_node = markdown_to_html_root_node(md)
        html = root_node.to_html()
        self.assertEqual(
            html,
            "<html><head></head><body><pre><code>This has `backticks` inside\nand **bold** should _not_ parse\n</code></pre></body></html>",
        )

    def test_unclosed_formatting(self):
        md = "This is **unclosed bold text"

        with self.assertRaises(Exception):
            root_node = markdown_to_html_root_node(md)
            html = root_node.to_html()

    def test_consecutive_formatting(self):
        md = "This is **bold**_italic_`code` text"

        root_node = markdown_to_html_root_node(md)
        html = root_node.to_html()
        self.assertIn("<b>bold</b>", html)
        self.assertIn("<i>italic</i>", html)
        self.assertIn("<code>code</code>", html)

    def test_empty_formatting(self):
        md = "This has ** ** and __ __ empty markers"

        with self.assertRaises(ValueError):
            root_node = markdown_to_html_root_node(md)
            html = root_node.to_html()

    def test_mixed_delimiters_in_code(self):
        md = """
```
const str = "**bold** and _italic_";
function test() { return `template ${var}`; }
```
"""

        root_node = markdown_to_html_root_node(md)
        html = root_node.to_html()
        self.assertIn("const str", html)
        self.assertNotIn("<b>", html)
        self.assertNotIn("<i>", html)

    def test_paragraph_with_multiple_code_blocks(self):
        md = "Use `code1` and `code2` in paragraph"

        root_node = markdown_to_html_root_node(md)
        html = root_node.to_html()
        self.assertIn("<code>code1</code>", html)
        self.assertIn("<code>code2</code>", html)

    def test_formatting_at_boundaries(self):
        md = "**start** text _end_"

        root_node = markdown_to_html_root_node(md)
        html = root_node.to_html()
        self.assertIn("<b>start</b>", html)
        self.assertIn("<i>end</i>", html)

    def test_whitespace_around_formatting(self):
        md = "text ** bold ** more"

        root_node = markdown_to_html_root_node(md)
        html = root_node.to_html()
        self.assertTrue(len(html) > 0)

    def test_special_characters_in_code(self):
        md = """
```
@#$%^&*()[]{}\\/<>?
|`~!@#$%^&*()
```
"""

        root_node = markdown_to_html_root_node(md)
        html = root_node.to_html()
        self.assertIn("@#$%^&*()", html)
        self.assertNotIn("<b>", html)


if __name__ == "__main__":
    unittest.main()
