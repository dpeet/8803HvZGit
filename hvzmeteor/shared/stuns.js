Stuns = new Mongo.Collection('stuns');

//TimeStamp, HumanID, ZombieID

if (Meteor.isServer){
    Stuns.allow({
        insert: function (userId, doc) {
            return true;
        },
        update: function (userId, doc, fieldNames, modifier) {
            return true;
        },
        remove: function (userId, doc) {
            return true;
        }
    });
}
