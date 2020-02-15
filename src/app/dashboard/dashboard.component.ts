import { Component, OnInit } from '@angular/core';
import { Race } from '../race';
import { Season } from '../season';
import { SeasonService } from '../season.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: [ './dashboard.component.css' ]
})
export class DashboardComponent implements OnInit {
  races: Race[] = [];
  seasons: Season[] = [];

  constructor(private seasonService: SeasonService) { }

  ngOnInit() {
    this.getRaces();
    this.getSeasons();
  }

  getRaces(): void {
    this.seasonService.getRaces()
      .subscribe(races => this.races = races.slice(1, 5));
  }

  getSeasons(): void {
    console.log("In getSeasons");
    this.seasonService.getSeasons()
      .subscribe(seasons => this.seasons = seasons.slice(1, 5));
  }
}
