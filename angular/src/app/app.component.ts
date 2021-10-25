import { Component, OnInit } from '@angular/core';
import sha256 from "fast-sha256";
import { LoginCredentials } from './api-objects/LoginCredentials';
import { DatabaseService } from './database.service';
import { LogInComponent } from './log-in/log-in.component';
import { LoginResponse } from './api-objects/LoginResponse';
import { RegistrationResponse } from './api-objects/RegistrationResponse';
import { RegistrationInfo } from './api-objects/RegistrationInfo';
import { EmailCheckResponse } from './api-objects/EmailCheckResponse';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})

export class AppComponent {
    title = 'angular';

    password = "";

    constructor(
        private databaseService: DatabaseService
    ) {}

    ngOnInit() {
        //testing connection to database
        this.login();
        this.register();
        this.checkEmail("fake_email@tes.gov");
    }

    login(): void {
        //test
        let credentials: LoginCredentials = {
            email: "fake_email@test.gov",
            password: this.hashPassword("thewrongpassword")
        }

        this.databaseService.login(credentials).subscribe((data: LoginResponse) => {
            console.log("Login response: " + data.response);
            if (data.response) {
                console.log("Login successful");
            }
            else {
                console.log("Login failed")
            }
        });
    }

    register(): void {
        //test
        let info: RegistrationInfo = {
            firstName: "Mayor",
            lastName: "Oana",
            gender: "female",
            email: "another_fake@flylo.fm",
            password: this.hashPassword("mypassword")
        }

        this.databaseService.register(info).subscribe((data: RegistrationResponse) => {
            console.log("Restration response: " + data.response);
            if (data.response) {
                console.log("Registered successfully");
            }
            else {
                console.log("Failed Registration")
            }
        });
    }

    checkEmail(email: string): void {
        //test
        this.databaseService.isEmailInUse(email).subscribe((data: EmailCheckResponse) => {
            console.log("Email " + email + ": " + data.response);
        });
    }

    hashPassword(password: string): string {
        let encoder = new TextEncoder();
        let view = encoder.encode(password);
        view = sha256(view);
        return this.hexEncode(view);
    }

    hexEncode(arr: Uint8Array){
        var hex;
        var result = "";

        arr.forEach( character => {
            //only use least significant 8 bits
            for(var i = 1; i >= 0; i--) {
                hex = (character >> (4 * i)) & 0xF;
                result += hex.toString(16);
            }
        });

        return result
    }
}
