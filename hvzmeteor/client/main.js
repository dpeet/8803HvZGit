import { Template } from 'meteor/templating';
import { ReactiveVar } from 'meteor/reactive-var';
import moment from 'moment-timezone';


import './main.html';

Template.hello.onCreated(function helloOnCreated() {
  // counter starts at 0
  this.counter = new ReactiveVar(0);
});

Template.hello.helpers({
  counter() {
    return Template.instance().counter.get();
  }
});

Template.hello.events({
  'click button'(event, instance) {
    // increment the counter when button is clicked
    Meteor.call("insertStun", moment().tz("America/Los_Angeles").format(), "Noah", "Devon ", function(error, result){
      console.log("calling")
      if(error){
        console.log("error", error);
      }
      if(result){

      }
    });
    instance.counter.set(instance.counter.get() + 1);
  },
});


Template.Stuns.helpers({
  stuns:function(){
    return Stuns.find();
  }
});
