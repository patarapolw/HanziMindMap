import QtQuick.Controls 1.4
import QtQuick.Window 2.1
import QtQml.Models 2.2
import QtQuick 2.7

Window {
    width: 800
    height: 500

    TableView {
        id: content
        anchors.fill: parent

        TableViewColumn {
            role: "item_id"
            title: "ID"
        }

        TableViewColumn {
            role: "vocab"
            title: "Vocabulary"
        }

        TableViewColumn {
            role: "ass_sounds"
            title: "Associated Sounds"
        }

        TableViewColumn {
            role: "ass_meanings"
            title: "Associated Meanings"
        }

        model: ListModel {
            id: model
        }

        Component.onCompleted: {
            var userVocabDump = pyUserVocab.get_dump
            for(var i=0; i<userVocabDump.length; i++){
                model.append({
                    item_id: userVocabDump[i][0],
                    vocab: userVocabDump[i][1],
                    ass_sounds: userVocabDump[i][2],
                    ass_meanings: userVocabDump[i][3]
                })
            }
        }
    }
}