import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Window 2.2
import QtQuick.Layouts 1.3
import QtQuick.Controls.Styles 1.4

ApplicationWindow {
    id: root
    title: "Hanzi Brainstorm"
    visible: true
    width: 600
    height: 400

    menuBar: MenuBar {
        Menu {
            title: "Vocabularies"
            MenuItem {
                text: "User database"
                onTriggered: {
                    console.log(py.dump_database[0][0])
                    var component = Qt.createComponent("dump.qml")
                    if( component.status != Component.Ready )
                    {
                        if( component.status == Component.Error )
                            console.debug("Error:"+ component.errorString() );
                        return; // or maybe throw
                    }
                    var window    = component.createObject(root)
                    window.show()
                }
            }
        }

        Menu {
            title: "Hanzi"
            MenuItem {
                text: "Do you know this character?"
                onTriggered: {
                    var component = Qt.createComponent("know_char.qml")
                    if( component.status != Component.Ready )
                    {
                        if( component.status == Component.Error )
                            console.debug("Error:"+ component.errorString() );
                        return; // or maybe throw
                    }
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
                property bool match: false

                id: char_vocab
                Layout.fillWidth: true
                background: Rectangle {
                    color: char_vocab.match ? "#badc58" : "#ffffff"
                }
                onTextEdited: {
                    py.text_changed(char_vocab.text)
                    var lookup = JSON.parse(py.lookup)

                    if(lookup.user){
                        ass_sounds.text = lookup.user[0]
                        ass_meanings.text = lookup.user[1]
                    } else {
                        ass_sounds.text = ''
                        ass_meanings.text = ''
                    }

                    if(lookup.dictionary){
                        dict_readings.text = "<a href='"+ char_vocab.text + "'>"
                            + lookup.dictionary[0].reading + "</a>"
                        dict_meanings.text = lookup.dictionary[0].english + "<br />"

                        if(lookup.dictionary.length > 1){
                            dict_meanings.text += "<br />Meaning " + 1 + " of "
                                + lookup.dictionary.length + " "
                            dict_meanings.text += "<a href='" + 1 + "'>Next meaning</a>"
                        }
                    } else {
                        dict_readings.text = ""
                        dict_meanings.text = ""
                    }

                    var sentence_text = ''
                    for(var i=0; i<lookup.sentence.length; i++){
                        sentence_text += "<a href='"+ lookup.sentence[i].sentence + "'>"
                            + lookup.sentence[i].sentence + "</a> "
                            + lookup.sentence[i].english + "<br />"
                    }
                    sentence.text = sentence_text

                    checkInDatabase()
                }
            }

            Label { text: "Associated sounds：" }
            TextField {
                property bool match: false

                id: ass_sounds
                Layout.fillWidth: true
                background: Rectangle {
                    color: ass_sounds.match ? "#badc58" : "#ffffff"
                }
                onTextEdited: {
                    checkInDatabase()
                }
            }

            Label { text: "Associated meanings：" }
            TextField {
                property bool match: false

                id: ass_meanings
                Layout.fillWidth: true
                background: Rectangle {
                    color: ass_meanings.match ? "#badc58" : "#ffffff"
                }
                onTextEdited: {
                    checkInDatabase()
                }
                onAccepted: {
                    submit.click()
                }
            }

            Label { text: "Readings：" }
            Text {
                id: dict_readings
                Layout.fillWidth: true
                wrapMode: Text.WordWrap
                textFormat: TextEdit.RichText
                onLinkActivated: {
                    py.speak(char_vocab.text)
                }
            }

            Label { text: "Meanings : "; Layout.alignment: Qt.AlignTop }
            ScrollView {
                implicitHeight: 100
                Layout.fillWidth: true

                TextArea {
                    id: dict_meanings
                    height: parent.height
                    Layout.fillWidth: true
                    wrapMode: Text.WordWrap
                    textFormat: TextEdit.RichText
                    readOnly: true
                    onLinkActivated: {
                        var lookup = JSON.parse(py.lookup)

                        dict_readings.text = "<a href='"+ char_vocab.text + "'>"
                            + lookup.dictionary[link].reading + "</a>"
                        dict_meanings.text = lookup.dictionary[link].english + "<br />"

                        dict_meanings.text += "<br />Meaning " + (parseInt(link)+1) + " of "
                            + lookup.dictionary.length + " "

                        if(link > 0){
                            dict_meanings.text += "<a href='" + (parseInt(link)-1) + "'>Previous meaning</a> "
                        }

                        if(link < lookup.dictionary.length-1){
                            dict_meanings.text += "<a href='" + (parseInt(link)+1) + "'>Next meaning</a>"
                        }
                    }
                }
            }

            Label { text: "Sentences："; Layout.alignment: Qt.AlignTop }
            ScrollView {
                implicitHeight: 100
                Layout.fillWidth: true

                TextArea {
                    id: sentence
                    Layout.fillWidth: true
                    wrapMode: Text.WordWrap
                    textFormat: TextEdit.RichText
                    readOnly: true
                    onLinkActivated: {
                        py.speak(link)
                    }
                }
            }
        }

        RowLayout {
            anchors.right: parent.right

            Button {
                id: submit
                text: "Submit Entry"
                enabled: false
                onClicked: {
                    py.do_submit(char_vocab.text, ass_sounds.text, ass_meanings.text)
                }
            }
            Button {
                id: remove
                text: "Remove Entry"
                enabled: false
                onClicked: {
                    py.do_delete(char_vocab.text)
                }
            }
            Button {
                id: clear
                text: "Clear"
                enabled: false
                onClicked: {
                    char_vocab.text = ass_sounds.text = ass_meanings.text = ""
                }
            }
        }
    }

    function checkInDatabase(){
        if(py.found){
            char_vocab.match = true
            remove.enabled = true
        } else {
            char_vocab.match = false
            remove.enabled = false
        }

        if(char_vocab.text && (ass_sounds.text || ass_meanings.text)){
            submit.enabled = true
        } else {
            submit.enabled = false
        }

        var lookup = JSON.parse(py.lookup)
        if("user" in lookup && lookup.user !== null){
            if(lookup.user[0] == ass_sounds.text){
                ass_sounds.match = true
            } else {
                ass_sounds.match = false
            }
            if(lookup.user[1] == ass_meanings.text){
                ass_meanings.match = true
            } else {
                ass_meanings.match = false
            }
        } else {
            ass_sounds.match = false
            ass_meanings.match = false
        }

        if(char_vocab.text || ass_sounds.text || ass_meanings.text){
            clear.enabled = true
        } else {
            clear.enabled = false
        }
    }
}