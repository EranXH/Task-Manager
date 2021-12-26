import ast
from Code.GlobalFunctions import StringTheListValues, GetListDifference, IntTheListValues, GetAllSerialNumbersFromRoutes

import time

# TODO: create a way to send inceapted messages from the server to the clint and from the clint to the server
#  using the key method


def ReplaceValuesByIndex(DataFrame, Index, ColumnName, NewValue):
    DataFrame.at[Index, ColumnName] = NewValue
    return DataFrame

def UpdateRowByDict(data_frame, new_values_dict , row_index):
    data_frame.loc[row_index, new_values_dict.keys()] = new_values_dict.values()
    return data_frame

def AppendRowByDict(data_fram, new_values_dict):
    return data_fram.append(new_values_dict, ignore_index=True)

# - YET TO BE USED -
def DeletGivenColumn(DataFrame, ColumnName):
    DataFrame.drop(ColumnName, axis=1, inplace=True)
    return DataFrame

def DeleteRowsByValueAndColumnName(data_frame, value, column_name):
    return data_frame[data_frame[column_name] != value]


def GetDataFrameFromIndexes(DataFrame, IndexesList):
    return DataFrame.loc[IndexesList].reset_index(drop=True)


# GetIdxListFromSerialNumList
def GetIdxListFromValuesList(DataFrame, ValuesList, ColumnName):
    # when creating a series the type of the serial numbers changes from str to int
    DFSerialNumbers = DataFrame[ColumnName]
    return [Idx for num in ValuesList
                    for Idx in DataFrame.index[DFSerialNumbers == num].tolist()]


def UpdateAssociatedTaskProgressVal(RoutesList, TasksDF, CheckListAmountOfCheckedItems, CheckListAmountOfItems):
    SerialNumberList = GetAllSerialNumbersFromRoutes(RoutesList)
    TasksIdxList = GetIdxListFromValuesList(TasksDF, SerialNumberList, "_id")
    TasksToUpdate = [task_idx for task_idx in TasksIdxList if not TasksDF.iloc[task_idx]['has_checklist']]
    TasksProgressColumn = TasksDF['progress']
    TasksProgressList = TasksDF['progress'].tolist()
    DictForProgColUpdate = {}
    for task_idx in TasksToUpdate:
        task_prog = ast.literal_eval(TasksProgressList[task_idx])
        checked_checklist_items = int(task_prog[0]) + CheckListAmountOfCheckedItems
        total_checklist_items = int(task_prog[1]) + CheckListAmountOfItems
        task_prog = [checked_checklist_items, total_checklist_items]
        DictForProgColUpdate[task_idx] = StringTheListValues([task_prog])[0]

    TasksProgressColumn.replace(DictForProgColUpdate)
    TasksDF.update(TasksProgressColumn)

    return TasksDF
