import wikipedia

def get_wiki_content(topic, language):
    wikipedia.set_lang(language)
    wiki_page = wikipedia.page(topic)
    return wiki_page.content.replace('==', '').split()

def break_into_groups(language, output_file, topic):
    try:
        words = get_wiki_content(topic, language)
        groups = []

        for i in range(0, len(words), 15):
            group = ' '.join(words[i:i + 15])
            groups.append(f"{language}|{group}")

        with open(output_file, 'w', encoding='utf-8') as file:
            for group in groups:
                if len(group.split()) == 15:
                    file.write(group + '\n')

        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False


if __name__ == '__main__':
    language = 'en'
    output_file = 'data/en.txt'
    topic = 'Cow'

    break_into_groups(language, output_file, topic)