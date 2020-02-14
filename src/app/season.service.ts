import { Injectable } from '@angular/core';
import { Race } from './race';
import { RACES } from './mock-races';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SeasonService {

  constructor() { }

  getRaces(): Observable<Race[]> {
    return of(RACES);
  }

  getRace(id: number): Observable<Race> {
    return of(RACES.find(race => race.id === id));
  }
}
