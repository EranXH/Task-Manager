# deletes all the widgets of a class (caled from UI`s)
# allows for no duplications
# helps to remove AttributeError and RuntimeError
class DeleteAllWidgets:
    def __init__(self, windows_widget_name):
        attrs = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        for attr in attrs:
            try:
                # checking that the window widget is not being deleted
                if attr != windows_widget_name:
                    getattr(self, attr).deleteLater()

            # AttributeError - non Pyqt5 widget object don't have attribute named "deleteLater"

            except AttributeError:
                pass

            # RuntimeError - wrapped C/C++ object of type Pyqt5 widget has been deleted
            except RuntimeError:
                pass
