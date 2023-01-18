from classes.Database import Database
from classes.Items import ArtistItem

db = Database("tests/Test.db")

table = "Artists"
columns = ["Name","Genre"]

result = db.select_from(table,columns)

expected = [["Conner","Funk"],["Conner2","Funk"]]

new = ArtistItem("125","ConnerAgain","Rock")
db.insert("Artists",new)

data = db.select_from("Artists",["Name","Genre"])

print(data)