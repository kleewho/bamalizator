import { Component, OnInit } from '@angular/core';
import { Race } from '../race';
import { SeasonService } from '../season.service';

@Component({
  selector: 'app-season',
  templateUrl: './season.component.html',
  styleUrls: ['./season.component.css']
})
export class SeasonComponent implements OnInit {
  races: Race[];

  getRaces(): void {
    this.seasonService.getRaces()
      .subscribe(races => this.races = races)
  }

  constructor(private seasonService: SeasonService) { }

  ngOnInit(): void {
    this.getRaces();
  }
}
// tytus
