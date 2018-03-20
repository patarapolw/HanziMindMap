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

            Label {
                property bool match: false
                color: match ? "green" : "black"

                id: character
                font.pointSize: 200
                Layout.preferredWidth: 200
                Layout.preferredHeight: 200
            }
            Label {
                text: "<a href='#'>Next character</a>"
                onLinkActivated: {
                    new_char(pyUserVocab.get_rand_char)
                }
            }
        }

        ColumnLayout {
            Label { text: "Related characters : "}
            TextField {
                property bool match: false
                background: Rectangle {
                    border.color: "gray"
                    color: rel_char.match ? "#badc58" : "#ffffff"
                }

                id: rel_char
                Layout.fillWidth: true
                onTextEdited: {
                    checkInDatabase()
                }
            }

            Label { text: "Related vocabularies : "}
            TextField {
                property bool match: false
                background: Rectangle {
                    border.color: "gray"
                    color: rel_vocab.match ? "#badc58" : "#ffffff"
                }

                id: rel_vocab
                Layout.fillWidth: true
                onTextEdited: {
                    checkInDatabase()
                }
                onAccepted: {
                    submit.click()
                }
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

        var rel_vocab_text = []
        var database = pyUserVocab.get_dump
        for(var i=0; i<database.length; i++){
            if(database[i].join().indexOf(character.text) != -1)
                rel_vocab_text.push(database[i][1])
        }
        rel_vocab.text = rel_vocab_text.join('，')

        var rel_sen_text = ''
        pyDictSentence.do_lookup(_char)
        var sen = JSON.parse(pyDictSentence.get_lookup)
        for(i=0; i<sen.length; i++){
            rel_sen_text += "<a href='"+ sen[i].sentence + "'>"
                            + sen[i].sentence + "</a> "
                            + sen[i].english + "<br />"
        }
        rel_sen.text = rel_sen_text

        pyUserHanzi.do_lookup(_char)
        var lookup = pyUserHanzi.get_lookup
        if(lookup.length === 2){
            rel_char.text = lookup[0]
            rel_vocab.text = lookup[1]
        } else {
            rel_char.text = ""
        }

        checkInDatabase()
    }

    function checkInDatabase() {
        var lookup = pyUserHanzi.get_lookup
        if(lookup.length === 2){
            character.match = true
            remove.enabled = true

            if(lookup[0] == rel_char.text){
                rel_char.match = true
            } else {
                rel_char.match = false
            }
            if(lookup[1] == rel_vocab.text){
                rel_vocab.match = true
            } else {
                rel_vocab.match = false
            }
        } else {
            character.match = false
            remove.enabled = false

            rel_char.match = false
            rel_vocab.match = false
        }

        if(rel_char.text || rel_vocab.text){
            submit.enabled = true
            clear.enabled = true
        } else {
            submit.enabled = false
            clear.enabled = false
        }
    }

    Component.onCompleted: {
        new_char(pyUserVocab.get_rand_char)
    }
}