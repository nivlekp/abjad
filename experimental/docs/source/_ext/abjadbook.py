import docutils.nodes


def strip_prompt(text):
    result = []
    for line in text.splitlines():
        if line.startswith(('>>> ', '... ')):
            result.append(line[4:])
    return result


def process_doctree(app, doctree, docname):
    if app.config.abjadbook_should_process and \
        docname.startswith(app.config.abjadbook_transform_path):

        print ''
        print docname
        print '-' * 80

        literal_blocks = list(doctree.traverse(docutils.nodes.literal_block))
        all_lines = []
        has_show_command = False

        for literal_block in literal_blocks:
            lines = strip_prompt(literal_block[0])
            this_has_show_command = False
            for line in lines:
                if line.startswith('show('):
                    has_show_command = True
                    this_has_show_command = True
            all_lines.extend(lines)

            if this_has_show_command:
                warning = docutils.nodes.warning()
                paragraph = docutils.nodes.paragraph()
                message = 'abjad-book images will appear here!'
                text = docutils.nodes.Text(message, message)
                paragraph.append(text)
                warning.append(paragraph)
                literal_block.replace_self([literal_block, warning])

        if has_show_command:
            print '\n'.join(all_lines)

def setup(app):
    app.add_config_value('abjadbook_should_process', False, 'env')
    app.add_config_value('abjadbook_transform_path', 'api/tools/', 'env')
    app.connect('doctree-resolved', process_doctree)

