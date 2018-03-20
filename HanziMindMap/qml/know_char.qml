import QtQuick.Window 2.2
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.3
import QtQuick 2.7

Window {
    width: 600
    height: 400
    x: 200
    y: 200

    RowLayout {
        anchors.margins: 10
        anchors.fill: parent

        ColumnLayout {
            spacing: 20
            anchors.top: parent.top

            Text {
                id: character
                font.pointSize: 200
                Layout.preferredWidth: 200
                Layout.preferredHeight: 200
            }
            Text {
                text: "<a href='#'>Next character</a>"
                onLinkActivated: {
                    new_char(py.rand_char)
                }
            }
        }

        ColumnLayout {
            Label { text: "Related characters : "}
            TextField {
                id: rel_char
                Layout.fillWidth: true
            }

            Label { text: "Related vocabularies : "}
            TextField {
                id: rel_vocab
                Layout.fillWidth: true
            }

            Label { text: "Related sentences : "}
            ScrollView {
                implicitHeight: 200
                Layout.fillWidth: true

                TextArea {
                    id: rel_sen
                    height: parent.height
                    Layout.fillWidth: true
                    wrapMode: Text.WordWrap
                    textFormat: TextEdit.RichText
                    readOnly: true
                    onLinkActivated: {
                        py.speak(link)
                    }
                }
            }

            RowLayout {
                anchors.right: parent.right

                Button {
                    id: submit
                    text: "Submit Entry"
                    enabled: false
                }
                Button {
                    id: remove
                    text: "Remove Entry"
                    enabled: false
                }
                Button {
                    id: reset
                    text: "Reset"
                    onClicked: {
                        new_char(character.text)
                    }
                }
            }
        }
    }

    function new_char(_char) {
        character.text = _char
        py.text_changed(character.text)

        var rel_vocab_text = []
        var database = py.dump_database
        for(var i=0; i<database.length; i++){
            if(database[i].join().indexOf(character.text) != -1)
                rel_vocab_text.push(database[i][1])
        }
        rel_vocab.text = rel_vocab_text.join(', ')

        var rel_sen_text = ''
        var sen = JSON.parse(py.lookup).sentence
        for(i=0; i<sen.length; i++){
            rel_sen_text += "<a href='"+ sen[i].sentence + "'>"
                            + sen[i].sentence + "</a> "
                            + sen[i].english + "<br />"
        }
        rel_sen.text = rel_sen_text
    }

    Component.onCompleted: {
        new_char(py.rand_char)
    }
}