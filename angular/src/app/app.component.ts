import { Component, OnInit } from '@angular/core';
import sha256 from "fast-sha256";
import { LoginCredentials } from './api-objects/LoginCredentials';
import { DatabaseService } from './database.service';
import { LogInComponent } from './log-in/log-in.component';
import { TableList } from './TableList';
import { LoginResponse } from './api-objects/LoginResponse';

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
        this.login();
        //this.getTables();
    }

    getTables(): void{
        this.databaseService.retrieveTables()
            .subscribe((data: TableList) => console.log(data));
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
