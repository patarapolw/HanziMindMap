import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Window 2.2
import QtQuick.Layouts 1.3

ApplicationWindow {
    title: "Hanzi Mind Map"
    width: 600

//    menuBar: MenuBar {
//        Menu: {
//            title: "File"
//            MenuItem {
//                text: "Dump database"
////                onTriggered:
//            }
//            MenuItem {
//                text: "Do you know this character?"
////                onTriggered:
//            }
//        }
//    }

    ColumnLayout {
        GridLayout {
            columns: 2

            Label { text: "Char/Vocab：" }
            TextField {
                id: char_vocab
            }

            Label { text: "Associated sounds：" }
            TextField {
                id: ass_sounds
            }

            Label { text: "Associated meanings：" }
            TextField {
                id: ass_meanings
            }

            Label { text: "Readings：" }
            Label {
                id: readings
            }

            Label { text: "Meanings : " }
            Label {
                id: meanings
            }

            Label { text: "Sentences：" }
            Label {
                id: sentences
            }
        }

        RowLayout {
            Rectangle {}
            Button {
                id: submit
                text: "Submit Entry"
            }
            Button {
                id: remove
                text: "Remove Entry"
            }
            Button {
                id: clear
                text: "Clear"
            }
        }
    }
}