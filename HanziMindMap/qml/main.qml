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
    height: 400

    menuBar: MenuBar {
        Menu {
            title: "&File"
            MenuItem {
                text: "Dump database"
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
                property Rectangle search_found: Rectangle { color: "#badc58" }
                property Rectangle search_not_found: Rectangle { color: "#ffffff" }

                id: char_vocab
                Layout.fillWidth: true
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

                    if(py.found){
                        char_vocab.background = search_found
                        remove.enabled = true
                    } else {
                        char_vocab.background = search_not_found
                        remove.enabled = false
                    }

                    if(char_vocab.text){
                        submit.enabled = true
                        clear.enabled = true
                    } else {
                        submit.enabled = false
                        clear.enabled = false
                    }
                }
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
}