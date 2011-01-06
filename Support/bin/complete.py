#!/usr/bin/python
# encoding: utf-8
import textmate
from textmate import ui

# Import rope modules
try:
    from rope.base.project import Project
    try:
        from rope.contrib import codeassist
    except:
        textmate.exit_show_tool_tip('Cannot find rope.contrib.codeassist. Rope may need to be updated.')
except:
    textmate.exit_show_tool_tip('Rope module not found!')

def main():
    try:
        # TODO: Determine if this is necessary. Can we still provide basic completion in a 'standalone' file?
        if textmate.PROJECT_DIRECTORY is None:
            textmate.exit_show_tool_tip('No completions.')
            
        current_word = textmate.current_word(r"[\w_]*", 'both')

        f = open(textmate.FILEPATH, 'r')
        source = f.read()
        f.close()

        project = Project(textmate.PROJECT_DIRECTORY)
        resource = project.get_resource(textmate.FILEPATH.replace(textmate.PROJECT_DIRECTORY, '')[1:])
        caret_index = source.find(textmate.CURRENT_LINE) + textmate.LINE_INDEX
        
        completions = codeassist.code_assist(project, source, caret_index, resource)
        if len(completions) == 1:
            selection = completions[0].name
            textmate.exit_insert_text(selection.replace(current_word, '', 1))
        elif len(completions):
            completions = codeassist.sorted_proposals(completions)
            completions = [{'display': completion.name, 'insert': completion.name} for completion in completions]
            selection = ui.complete(completions, {'initial_filter': current_word, 'extra_chars': "_"})

        else:
            selection = None
            textmate.exit_show_tool_tip('No completions.')

    except Exception as e:
        textmate.exit_show_tool_tip('ERROR %s: %s' % (type(e), e))


# def goto_definition(self):
#     """
#     Tries to find the definition for the currently selected scope;
# 
#         * if the definition is found, returns a tuple containing the file path and the line number (e.g. ``('/Users/fabiocorneti/src/def.py', 23))``
#         * if no definition is found, returns None
# 
#     """
#     #TODO: support multiple matches
#     if TM_PROJECT_DIRECTORY is None:
#         return None
#     project = Project(TM_PROJECT_DIRECTORY)
#     caret_index = self.source.find(TM_CURRENT_LINE) + TM_LINE_INDEX
#     resource, line = codeassist.get_definition_location(project, self.source, caret_index)
#     if resource is not None:
#         return 'txmt://open?url=file://%s&line=%d' % (urllib.quote(resource.real_path), line)
#     else:
#         return ''

if __name__ == "__main__":
    main()


