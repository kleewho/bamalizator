import { Component, OnInit } from '@angular/core';
import { Race } from '../race';
import { SeasonService } from '../season.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: [ './dashboard.component.css' ]
})
export class DashboardComponent implements OnInit {
  races: Race[] = [];

  constructor(private seasonService: SeasonService) { }

  ngOnInit() {
    this.getHeroes();
  }

  getHeroes(): void {
    this.seasonService.getRaces()
      .subscribe(races => this.races = races.slice(1, 5));
  }
}
