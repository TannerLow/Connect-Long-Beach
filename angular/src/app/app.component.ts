import { Component,OnInit } from '@angular/core';
import sha256 from "fast-sha256";
import { DatabaseService } from './database.service';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})

export class AppComponent {
    //title = 'angular';

    password = "";
    table:String = "";

    constructor(
        private databaseService: DatabaseService
    ) {}

    ngOnInit(){this.getTables() }

    getTables(): void{
        this.databaseService.retrieveTables().subscribe(table => this.table = table);
    }


    submitCredentials() {
        let encoder = new TextEncoder();
        let view = encoder.encode(this.password);
        view = sha256(view);
        let decoder = new TextDecoder();
        let str = decoder.decode(view);
        console.log(str);
        console.log(this.hexEncode(view));
        
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
