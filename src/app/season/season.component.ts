import { Component, OnInit } from '@angular/core';
import { Race } from '../race'
import { RACES } from '../mock-races';

@Component({
  selector: 'app-season',
  templateUrl: './season.component.html',
  styleUrls: ['./season.component.css']
})
export class SeasonComponent implements OnInit {
  races = RACES;
  selectedRace: Race;
  onSelect(race: Race): void {
    this.selectedRace = race;
  }

  constructor() { }

  ngOnInit(): void {
  }
}
