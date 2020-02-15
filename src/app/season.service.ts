import { Injectable } from '@angular/core';
import { Race } from './race';
import { Season } from './season';
import { Observable, of } from 'rxjs';
import s2019 from '../assets/seasons/2019.json';
import s2020 from '../assets/seasons/2020.json';

@Injectable({
  providedIn: 'root'
})
export class SeasonService {

  constructor() { }

  allRaces = s2019.races.concat(s2020.races);

  getSeason(year: number): Observable<Season> {

    return s2019;
  }

  getRaces(): Observable<Race[]> {
    return of(s2019.races);
  }

  getRace(id: number): Observable<Race> {
    return of(this.allRaces.find(race => race.id === id));
  }
}
