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
                    openNewWindow("vocab_dump.qml")
                }
            }
            MenuSeparator {}
            MenuItem {
                text: "Statistics"
//                onTriggered: {
//                    openNewWindow("hanzi_know.qml")
//                }
            }
        }

        Menu {
            title: "Hanzi"
            MenuItem {
                text: "Do you know this Hanzi?"
                onTriggered: {
                    openNewWindow("hanzi_know.qml")
                }
            }
            MenuItem {
                text: "User database"
//                onTriggered: {
//                    openNewWindow("hanzi_know.qml")
//                }
            }
            MenuSeparator {}
            MenuItem {
                text: "Statistics"
//                onTriggered: {
//                    openNewWindow("hanzi_know.qml")
//                }
            }
        }

        Menu {
            title: "About"
            MenuItem {
                text: "About Hanzi Brainstorm"
//                onTriggered: {
//                    openNewWindow("hanzi_know.qml")
//                }
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
                    border.color: "gray"
                    color: char_vocab.match ? "#badc58" : "#ffffff"
                }
                onTextEdited: {
                    pyUserVocab.do_lookup(char_vocab.text)
                    pyDictVocab.do_lookup(char_vocab.text)
                    pyDictSentence.do_lookup(char_vocab.text)
                    var lookup_user = pyUserVocab.get_lookup
                    var lookup_dictionary = JSON.parse(pyDictVocab.get_lookup)
                    var lookup_sentence = JSON.parse(pyDictSentence.get_lookup)

                    if(lookup_user.length === 2){
                        ass_sounds.text = lookup_user[0]
                        ass_meanings.text = lookup_user[1]
                    } else {
                        ass_sounds.text = ''
                        ass_meanings.text = ''
                    }

                    if(lookup_dictionary.length !== 0){
                        dict_readings.text = "<a href='"+ char_vocab.text + "'>"
                            + lookup_dictionary[0].reading + "</a>"
                        dict_meanings.text = lookup_dictionary[0].english + "<br />"

                        if(lookup_dictionary.length > 1){
                            dict_meanings.text += "<br />Meaning " + 1 + " of "
                                + lookup_dictionary.length + " "
                            dict_meanings.text += "<a href='" + 1 + "'>Next meaning</a>"
                        }
                    } else {
                        dict_readings.text = ""
                        dict_meanings.text = ""
                    }

                    var sentence_text = ''
                    for(var i=0; i<lookup_sentence.length; i++){
                        sentence_text += "<a href='"+ lookup_sentence[i].sentence + "'>"
                            + lookup_sentence[i].sentence + "</a> "
                            + lookup_sentence[i].english + "<br />"
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
                    border.color: "gray"
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
                    border.color: "gray"
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
                        var lookup_dictionary = JSON.parse(pyDictVocab.get_lookup)

                        dict_readings.text = "<a href='"+ char_vocab.text + "'>"
                            + lookup_dictionary[link].reading + "</a>"
                        dict_meanings.text = lookup_dictionary[link].english + "<br />"

                        dict_meanings.text += "<br />Meaning " + (parseInt(link)+1) + " of "
                            + lookup_dictionary.length + " "

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
                    pyUserVocab.do_submit(char_vocab.text, ass_sounds.text, ass_meanings.text)
                }
            }
            Button {
                id: remove
                text: "Remove Entry"
                enabled: false
                onClicked: {
                    pyUserVocab.do_delete(char_vocab.text)
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

    function openNewWindow(qml) {
        var component = Qt.createComponent(qml)
        if( component.status != Component.Ready )
        {
            if( component.status == Component.Error )
                console.debug("Error:"+ component.errorString() );
            return; // or maybe throw
        }
        var window    = component.createObject(root)
        window.show()
    }

    function checkInDatabase(){
        var lookup = pyUserVocab.get_lookup
        if(lookup.length === 2){
            char_vocab.match = true
            remove.enabled = true

            if(lookup[0] == ass_sounds.text){
                ass_sounds.match = true
            } else {
                ass_sounds.match = false
            }
            if(lookup[1] == ass_meanings.text){
                ass_meanings.match = true
            } else {
                ass_meanings.match = false
            }
        } else {
            char_vocab.match = false
            remove.enabled = false

            ass_sounds.match = false
            ass_meanings.match = false
        }

        if(char_vocab.text && (ass_sounds.text || ass_meanings.text)){
            submit.enabled = true
        } else {
            submit.enabled = false
        }

        if(char_vocab.text || ass_sounds.text || ass_meanings.text){
            clear.enabled = true
        } else {
            clear.enabled = false
        }
    }
}