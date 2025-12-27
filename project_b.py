import xml.etree.ElementTree as ET
import re

# DO NOT MODIFY THIS FUNCTION!
def check_tag_index(tags, tag_text):
	"""
	Determine the index of a given tag string within a list of tag strings. Returns -1 if the tag string is not found in the list of strings.

	Parameters
	----------
	tags : list of strings
		The list of strings (called tags) that have been compiled so far.
	tag_text : string
		The current tag to be searched for in the list of strings.

	Returns
	-------
	int
		Returns -1 if the tag is not found in the list of tags, and returns the index in the list where the tag is found otherwise.
	"""
	try:
		ix = tags.index(tag_text)
		return ix
	except:
		return -1

# DO NOT MODIFY THIS FUNCTION!
def load_messages(filename):
	"""
	Load messages sent to other users in the Python Slack channel and return the messages as a list.

	Parameters
	----------
	filename : string
		The current path to the XML file containing the message information.

	Returns
	-------
	messages : list of strings
		List of all the messages read from the XML file, one message per list element.
	"""
	tree = ET.parse(filename)
	root = tree.getroot()

	messages = []
	for message_node in root.iter('message'):
		text = message_node.find('text')
		messages.append(text.text)

	return messages

def get_num_messages(messages):
	return len(messages)

def get_message(messages, ix):
	return messages[ix]

def concatenate_messages(messages, ix1, ix2, separator):
	return separator.join([messages[ix1], messages[ix2]])

def get_message_num_words(messages):
	return [len(i.split()) for i in messages]

def get_message_avg_word_lengths(messages):
    avg_lengths = []
    for msg in messages:
        words = msg.split()
        if len(words) == 0:
            avg_lengths.append(0)
        else:
            total_chars = 0
            for w in words:
                total_chars += len(w)
            avg_lengths.append(total_chars/ len(words))
    return avg_lengths
    
                
def search_messages(messages, search_term, is_case_sensitive):
    messages_index = []
    in_messages_index = []
    
    for i in range(len(messages)):
        msg = messages[i]
        k = 0
        while k <= len(msg) - len(search_term):
            search_area = msg[k:k + len(search_term)]
            if is_case_sensitive:
                match = (search_area == search_term)
            else:
                match = (search_area.lower() == search_term.lower())
            
            if match:
                in_messages_index.append(k)
                messages_index.append(i)
                k += len(search_term)
            else:
                k += 1
    return messages_index, in_messages_index     

def replace_search_word_in_messages(messages, search_term, replacement, is_case_sensitive):
	
    replacements = 0
    
    for i in range(len(messages)):
        msg = messages[i]
        
        msg_index, in_msg_index = search_messages([msg], search_term, is_case_sensitive)
        
        if not in_msg_index:
            continue
        
        new_msg = ""
        last_index = 0
        
        for index in in_msg_index:
            new_msg += msg[last_index:index]
            
            new_msg += replacement
            last_index = index + len(search_term)
            replacements += 1
        new_msg += msg[last_index:]
        messages[i] = new_msg
        
    return replacements
        
        
def count_tagged_people(messages):
    tagged_people = []
    tag_index = []
    
    for message in messages:
        tags = re.findall(r'<@.+?>', message)
        for tag in tags:
            tag_ix = check_tag_index(tagged_people, tag)
            if tag_ix == -1:
                tagged_people.append(tag)
                tag_index.append(1)
            else:
                tag_index[tag_ix] += 1
    return tagged_people, tag_index

def generate_productivity_report(messages):
    num_messages = get_num_messages(messages)
    print(f'There are {num_messages} messages in the database.')
    
    words_per_message = get_message_num_words(messages)
    total_words = 0
    for count in words_per_message:
        total_words += count
    avg_words = total_words / len(words_per_message)
    print(f'Average words per message: {avg_words:.2f}.')
    
    avg_word_lengths_per_msg = get_message_avg_word_lengths(messages)
    total_word_length = 0
    for avg_len in avg_word_lengths_per_msg:
        total_word_length += avg_len
    avg_word_length_overall = total_word_length / len(avg_word_lengths_per_msg)
    print(f'Average word length overall: {avg_word_length_overall:.2f}.')
    
    tags, tag_counts = count_tagged_people(messages)
    
    max_count = 0
    max_index = 0
    
    for i in range(len(tag_counts)):
        if tag_counts[i] > max_count:
            max_count = tag_counts[i]
            max_index = i
    print(f'The person tagged the most is: {tags[max_index]} with {max_count} tags.')



if __name__ == '__main__':
	# Retrieve all the messages from the XML file.
	messages = load_messages('merged-pythondev-help.xml')

	generate_productivity_report(messages)