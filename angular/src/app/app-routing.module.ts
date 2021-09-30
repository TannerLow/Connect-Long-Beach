import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RoutingExampleComponent } from './routing-example/routing-example.component';

const routes: Routes = [
    { path: 'example', component: RoutingExampleComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

export const routingComponents = []