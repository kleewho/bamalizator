import { Injectable } from '@angular/core';
import { Race } from './race';
import { Season } from './season';
import { Observable, of } from 'rxjs';
import s2019 from '../assets/seasons/2019.json';

@Injectable({
  providedIn: 'root'
})
export class SeasonService {

  constructor() { }


  getSeason(year: number): Observable<Season> {
    return s2019;
  }

  getRaces(): Observable<Race[]> {
    return of(s2019.races);
  }

  getRace(id: number): Observable<Race> {
    return of(s2019.races.find(race => race.id === id));
  }
}
