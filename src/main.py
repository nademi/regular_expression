### Student : Yousef Nademi
### Student ID: 1492308
### ccid : nademi


import sys
import pandas as pd
import nltk


def data_read(dir_path, grammar_path):
    """
    This function will read the tsv training data and
    will convert it into a dataframe for dataprocessing.
    Input:
    dir_path[string/path]: the full path for the file incluiding the file name
    ex. (data/train.tsv)
    grammar_path[string/path] : the full path to the grammar file
    ex. (grammars/toy.cfg)
    Return:
    training_data_df[dataframe]: A pandas dataframe created based on the
    training data
    """
    # getting the names of all files in the directory and create a list for them
    df = pd.read_csv(dir_path, sep='\t', lineterminator='\r', skipinitialspace=True)
    #This will get rid of \n in the columns of df
    df = df.replace('\n', '', regex=True)
    df = df.dropna()
    grammar = nltk.data.load('file:toy.cfg')

    return df, grammar


def grammar_checker(df, simple_grammar):
    """[This function will parse POS tags included in the df
    based on the provided grammar]
    Input:
    df[pandas dataframe]: df to be processed by the grammar
    simple_grammar[str]: The grammar strings to check the POS tags
    Return:
    output_df[pandas dataframe] = processed dataframe
    [id, ground_truth, prediction]

    """
    sent_id = []
    ground_truth = []
    prediction = []
    parser = nltk.ChartParser(simple_grammar)
    for i in range(len(df)):
        sent_id.append(df['id'][i])
        ground_truth.append(df['label'][i])
        wrong_syntax = 1
        for tree in parser.parse(df['pos'][i].split()):
            #tree.pretty_print()
            wrong_syntax = 0
            if wrong_syntax == 1:
                print("Wrong Grammer!!!!!!")
    prediction.append(wrong_syntax)

    output_df = pd.DataFrame({'id': sent_id, 'ground_truth': ground_truth, 'prediction': prediction})
    return output_df


def precision_recall(output_df):
    """This function will caculate the precision and recall
    for the proccesed dataframe
    Input:
    output_df[pandas dataframe]: the processed dataframe
    Return:
    precision[float]
    recall [float]
    FP : False Positive
    TP : True Positive
    FN : False Negative
    TN : True Negative
    """

    FP = len(output_df[(output_df['ground_truth'] == 1) & (output_df['prediction'] == 0)])
    TP = len(output_df[(output_df['ground_truth'] == 0) & (output_df['prediction'] == 0)])
    FN = len(output_df[(output_df['ground_truth'] == 0) & (output_df['prediction'] == 1)])
    TN = len(output_df[(output_df['ground_truth'] == 1) & (output_df['prediction'] == 1)])
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    return precision, recall, FP, TP, FN, TN



def main():
    '''
    main function where the training data as well as the grammar file will be read and
    the processed data will be write in the provided path
    '''
    # the path to the input training data
    dir_path = sys.argv[1]
    # the path to the grammar file
    grammar_path = sys.argv[2]
    # the path that we want to write the output
    output_path = sys.argv[3]
    
    # Reading the data in the provided path and create a df for data processing
    df, grammar = data_read(dir_path, grammar_path)
    # This function will check the df and and create the output df
    output_df = grammar_checker(df, grammar)
    # This will calculate the parameters for the report including precision and recall
    # for the CFG
    precision, recall, FP, TP, FN, TN = precision_recall(output_df)
    print(f'The precision for our dataframe is {precision}; The recall is {recall}')
    print(f'The FP = {FP}; The TP = {TP}; FN = {FN}; TN = {TN} ')

    ##-----------------save output df to a tsv file-------------------------##
    output_df.to_csv(output_path, sep='\t')


if __name__ == "__main__":
    main()