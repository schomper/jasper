import os
import sys

JASPER = '~/Projects/jasper/'
ALPHA = 0.02


def clean_process_print(num_topics, num_words, working_dir):
    print('Cleaning Format File')
    os.system(JASPER + '2_before/clean_format_file.py '
                     + working_dir + '/initial.formatted '
                     + working_dir + '/c_lda.formatted')

    print('Processing LDAs')
    os.system(JASPER + '3_processing/lda est '
                     + str(ALPHA) + ' ' + str(num_topics) + ' '
                     + working_dir + '/settings '
                     + working_dir + '/c_lda.formatted random '
                     + working_dir + '/out')

    print('Printing Topics')
    os.system(JASPER + '5_after/print_topics.py '
                     + working_dir + '/out/final.beta '
                     + working_dir + '/initial.vocab '
                     + str(num_words) + ' ' + working_dir)


def main():
    if len(sys.argv) != 2:
        print('./auto_runner.py <working_dir>')
        exit(1)

    working_dir = sys.argv[1]

    os.system(JASPER + '2_before/gen_vocab_file.py '
                     + working_dir + '/clean.d '
                     + working_dir + '/initial')

    num_topics = eval(input("Select the number of topics: "))
    num_words = eval(input("Select the number of words to print: "))

    clean_process_print(num_topics, num_words, working_dir)

    lowest_significant = eval(input("Select the lowest significant num: "))

    print('Generating sub topics')
    os.system(JASPER + '4_hierarchy/gen_sub_topics.py '
                     + working_dir + '/out/final.gamma '
                     + working_dir + '/initial.formatted '
                     + lowest_significant + ' ' + num_topics + ' '
                     + working_dir + '/hierarchy')

    for index in range(0, num_topics):
        os.system(JASPER + '4_hierarchy/reindex_files.py '
                         + working_dir + '/hierarchy' + str(index) + '.txt '
                         + working_dir + '/initial.vocab '
                         + working_dir + '/' + str(index) + '/initial')

        this_working_dir = working_dir + '/' + str(index)

        this_num_topics = eval(input("Select the number of " +
                                     "topics for topic %d: " % index))

        num_words = eval(input("Select the number of words to print: "))

        clean_process_print(this_num_topics, num_words, this_working_dir)


if __name__ == '__main__':
    main()
