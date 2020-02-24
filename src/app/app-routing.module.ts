import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SeasonComponent } from './season/season.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { RaceComponent } from './race/race.component';

const routes: Routes = [
  { path: '', redirectTo: '/season', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'season', component: SeasonComponent },
  { path: 'detail/:id', component: RaceComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
