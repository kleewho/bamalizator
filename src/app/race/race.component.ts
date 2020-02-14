import { Component, OnInit, Input } from '@angular/core';
import { Race } from '../race';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { SeasonService } from '../season.service';

@Component({
  selector: 'app-race',
  templateUrl: './race.component.html',
  styleUrls: ['./race.component.css']
})
export class RaceComponent implements OnInit {
  @Input() race: Race;

  constructor(private route: ActivatedRoute,
              private seasonService: SeasonService,
              private location: Location) { }

  ngOnInit(): void {
    this.getRace();
  }

  getRace(): void {
    const id = +this.route.snapshot.paramMap.get('id');
    this.seasonService.getRace(id)
      .subscribe(race => this.race = race);
  }

}
