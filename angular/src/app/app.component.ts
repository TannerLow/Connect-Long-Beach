import { Component } from '@angular/core';
import { LogInComponent } from './log-in/log-in.component';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})

export class AppComponent {
    title = 'angular';

    password = "";

    constructor() {}

    ngOnInit() {

    }

    // test to show cross component variables, specifically user ID
    getUID() {
        if(LogInComponent.loggedIn){
            console.log("user id from retrieval: " + LogInComponent.userID);
        }
    }
}
