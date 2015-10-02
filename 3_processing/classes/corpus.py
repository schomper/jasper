from classes import document

class Corpus:
    def __init__(self, folder_name):

        #print("Initiating Corpus...")
        index = 2
        self.doc_list = []
        self.num_terms = 0
        self.num_docs = 0

        with open(folder_name, "r") as document_list:

            # for each document
            for doc in document_list:
                doc = doc.strip()

                # Get the amount of unique words in this document
                split_results = doc.split('|~|')
                attempt_split = split_results[3 + index].split(' ', 1)

                if len(attempt_split) == 1:
                    print('Skipping doc: ' + doc)
                    continue

                num_words, rest = attempt_split
                num_words = int(num_words)

                doc = document.Document(num_words, split_results[0 + index], split_results[1 + index], split_results[2 + index])
                
                print('rest: ' + rest)
                # for each word
                for word_index in range(0, num_words):

                    # get that specific word:count pair
                    if word_index < num_words - 1:
                        pair, rest = rest.split(' ', 1)
                    else:
                        pair = rest

                    # Split pair into word and count
                    print(pair)
                    word, count = pair.split(':')
                    word = int(word)
                    count = int(count)

                    # add pair to the document
                    doc.add_pair(word_index, word, count)

                    if word >= self.num_terms:
                        self.num_terms = word + 1

                # increase number of docs
                self.doc_list.append(doc)
                self.num_docs += 1

        print("Number of docs    : %d" % self.num_docs)
        print("Number of terms   : %d" % self.num_terms)

    def max_length(self):

        max_length = 0
        for doc_index in range(0, self.num_docs):
            if self.doc_list[doc_index].unique_word_count > max_length:
                max_length = self.doc_list[doc_index].unique_word_count

        return max_length
