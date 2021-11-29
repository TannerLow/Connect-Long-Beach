import { Component } from '@angular/core';
import { LogInComponent } from './log-in/log-in.component';
import { GlobalConstants} from './common/global-constants';


@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})

export class AppComponent {
    title = 'angular'
    signalButton: string;

    password = ""

    constructor() {
      this.signalButton= GlobalConstants.activeButton
    }

    ngOnInit() {
      console.log("hello "+this.signalButton)
    }

    // test to show cross component variables, specifically user ID
    getUID() {
        if(LogInComponent.loggedIn){
            console.log("user id from retrieval: " + LogInComponent.userID);
        }
        else {
            console.log("user not logged in")
        }
        return LogInComponent.userID;
    }
}
