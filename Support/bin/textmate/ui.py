import re
import textmate
import tempfile, plistlib, subprocess, sys, os

# TODO: rewrite this as pydoc
# Interactive Code Completion Selector
# Displays the pop-up completion menu with the list of +choices+ provided.
# 
# +choices+ should be an array of dictionaries with the following keys:
# 
# * +display+ -- The title to display in the suggestions list
# * +insert+  -- Snippet to insert after selection
# * +image+   -- An image name, see the <tt>:images</tt> option
# * +match+   -- Typed text to filter on (defaults to +display+)
# 
# All options except +display+ are optional.
# 
# +options+ is a hash which can accept the following keys:
#
# * <tt>:extra_chars</tt>       -- by default only alphanumeric characters will be accepted,
#   you can add additional characters to the list with this option.
# 	This string is escaped for regex. List each character in a simple string EG: '{<#^'
# * <tt>:case_insensitive</tt>  -- ignore case when filtering
# * <tt>:static_prefix</tt>     -- a prefix which is used when filtering suggestions.
# * <tt>:initial_filter</tt>    -- defaults to the current word
# * <tt>:images</tt>            -- a +Hash+ of image names to paths
# 
# If a block is given, the selected item from the +choices+ array will be yielded
# (with a new key +index+ added, which is the index of the +choice+ into the +choices+ array)
# and the result of the block inserted as a snippet
def complete(choices, options = {}, block = None):
    if '2' not in textmate.DIALOG:
        raise 'Dialog2 not found.'
    
    characters = 'a-zA-Z0-9'
    if 'extra_chars' in options:
        characters += re.escape(options['extra_chars'])
        
    if 'initial_filter' not in options:
        options['initial_filter'] = textmate.current_word(characters, "left")

    command = [textmate.DIALOG, "popup"]
    if "initial_filter" in options:
        command.append("--alreadyTyped %s" % textmate.sh_escape(options["initial_filter"]))
    if "static_prefix" in options:
        command.append("--staticPrefix %s" % textmate.sh_escape(options["static_prefix"]))
    if "extra_chars" in options:
        command.append("--additionalWordCharacters %s" % textmate.sh_escape(options['extra_chars']))
    if "case_insensitive" in options:
        command.append("--caseInsensitive")

    def formalize(choice):
        try:
            choice['display']
            choice['insert']
            return choice
        except (KeyError, IndexError, TypeError):
            return {'display': choice, 'insert' : choice}
    
    choices = [formalize(choice) for choice in choices]
    
    plist = {'suggestions': choices}

    result = None

    try:
        f = tempfile.NamedTemporaryFile()
        plistlib.writePlist(plist, f)
        f.seek(0)

        # command = [textmate.DIALOG, 'popup', '--suggestions', '({display = test; insert = tesinsert; }, {display = testinger; })']
        command.append('--returnChoice')

        DEVNULL = os.open(os.devnull, os.O_RDWR)
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=DEVNULL, stderr=DEVNULL)
        process.stdin.write(f.read())


        textmate.exit_show_tool_tip(','.join(command))
        
        # TODO: How to prevent the command from inserting the result??
        

        # # Deserialize the result dictionary
        # resultDict = {}
        # lines = result.split('\n')
        # for line in lines:
        #     if '=' in line:
        #         key, value = line.split('=')  
        #         resultDict[key.strip()] = re.sub(';', '', value.strip())
        #     
        # result = resultDict
    except Exception as e:
        textmate.exit_show_tool_tip('ERROR: %s' % e)
    finally:
        f.close()
    

    # Use a default block if none was provided
    # if not block:
    #     block = lambda choice:\
    #         choice['insert'] if choice else None

    # The block should return the text to insert as a snippet
    # to_insert = block.__call__(result)
    
    # return to_insert
    # if to_insert:
    #     textmate.sh("%s x-insert --snippet %s" % (textmate.DIALOG,
    #         textmate.sh_escape(to_insert)))
    # 
