# pip install cx_freeze
import cx_Freeze
executaveis = [ 
               cx_Freeze.Executable(script="main.py", icon="assets/icone.ico") ]
cx_Freeze.setup(
    name = "Iron Man",
    options={
        "build_exe":{
            "packages":["pygame"],
            "include_files":["assets"]
        }
    }, executables = executaveis
)

# python setup.py build
# python setup.py bdist_msi
