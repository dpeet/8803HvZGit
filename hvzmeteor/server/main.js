import { Meteor } from 'meteor/meteor';

Meteor.startup(() => {
  // code to run on server at startup
});

Meteor.methods({
    insertStun: function (TimeStamp, HumanID, ZombieID) {
      Stuns.insert({
        TimeStamp:TimeStamp,
        HumanID:HumanID,
        ZombieID:ZombieID
      });
    }
  })
