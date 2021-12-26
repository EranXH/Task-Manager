from pandas import DataFrame

from icecream import ic


# an inheritable object which organize the DataFrames
class OrganizeDFValues:
    def Organize(self, TasksDFs: tuple[DataFrame, DataFrame], TreeDFs: tuple[DataFrame, DataFrame], PrivateOrPublic):
        self.TasksDFs, self.TreeDFs = TasksDFs, TreeDFs

        self.PublicTasksDF, self.PrivateTasksDF = TasksDFs
        self.PublicTreeDF, self.PrivateTreeDF = TreeDFs

        self.GetPoPFittedDF(PrivateOrPublic)

        self.PublicIDToRouteDict = self.IDToRouteDict(self.PublicTreeDF, self.PublicTasksDF)
        self.PrivateIDToRouteDict = self.IDToRouteDict(self.PrivateTreeDF, self.PrivateTasksDF)

    # P - Private | o - or | P - Public
    def GetPoPFittedDF(self, PrivateOrPublic):
        # PrivateOrPublic = True (when Private) | PrivateOrPublic = False (when Public)
        self.PrivateOrPublic = PrivateOrPublic

        if PrivateOrPublic == 'Private':
            self.TasksDF, self.TreeDF = self.PrivateTasksDF, self.PrivateTreeDF
        else:
            self.TasksDF, self.TreeDF = self.PublicTasksDF, self.PublicTreeDF

    @staticmethod
    def IDToRouteDict(TreeDF, TasksDF):
        try:
            tasks_ids = TasksDF['_id'].tolist()
        except KeyError:
            tasks_ids = []

        id_to_routes_dict = {_id: [] for _id in tasks_ids}
        routes_list = TreeDF['URL']

        for index, ids in enumerate(TreeDF['IDs'].tolist()):
            for _id in ids:
                route = routes_list[index]
                id_to_routes_dict[_id].append(route)

        return id_to_routes_dict
