import { Race } from './race';

export interface Season {
  year: number;
  participants: number;
  races: Race[];
}
