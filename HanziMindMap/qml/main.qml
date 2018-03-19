import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Window 2.2
import QtQuick.Layouts 1.3
import QtQuick.Controls.Styles 1.4

ApplicationWindow {
    id: root
    title: "Hanzi Mind Map"
    visible: true
    width: 600
    minimumHeight: 400

    menuBar: MenuBar {
        Menu {
            title: "&File"
            MenuItem {
                text: "Dump database"
                onTriggered: {
                    var component = Qt.createComponent("dump.qml")
                    var window    = component.createObject(root)
                    window.show()
                }
            }
            MenuItem {
                text: "Do you know this character?"
                onTriggered: {
                    var component = Qt.createComponent("dump.qml")
                    var window    = component.createObject(root)
                    window.show()
                }
            }
        }
    }

    ColumnLayout {
        id: main
        anchors.fill: parent
        anchors.margins: 10

        GridLayout {
            columns: 2
            anchors.fill: parent

            Label { text: "Char/Vocab：" }
            TextField {
                id: char_vocab
                Layout.fillWidth: true
            }

            Label { text: "Associated sounds：" }
            TextField {
                id: ass_sounds
                Layout.fillWidth: true
            }

            Label { text: "Associated meanings：" }
            TextField {
                id: ass_meanings
                Layout.fillWidth: true
            }

            Label { text: "Readings：" }
            TextArea {
                id: readings
                implicitHeight: 40
            }

            Label { text: "Meanings : " }
            TextArea {
                id: meanings
                implicitHeight: 100
            }

            Label { text: "Sentences：" }
            TextArea {
                id: sentences
                implicitHeight: 60
            }
        }

        RowLayout {
            anchors.right: parent.right

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