import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SignUpComponent } from './sign-up/sign-up.component';
import {LogInComponent} from "./log-in/log-in.component";
import {ProfileComponent} from "./profile/profile.component";
import { HomePageComponent } from './home-page/home-page.component';
import {EmailCreationComponent} from "./email-creation/email-creation.component";

const routes: Routes = [
  {path: '', redirectTo:'/log-in', pathMatch:"full"},
  {path: 'sign-up', component: SignUpComponent},
  {path: 'log-in', component: LogInComponent},
  {path: 'profile', component: ProfileComponent},
  {path: 'home-page', component: HomePageComponent},
  {path: 'email-creation', component: EmailCreationComponent}
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

export const routingComponents = []
