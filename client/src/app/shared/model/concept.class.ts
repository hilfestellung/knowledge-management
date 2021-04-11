import {Label} from "./label.class";
import {Property} from "./property.class";

export interface Concept {
  id: string;
  labels?: Label[];
  properties?: Property[];
}
