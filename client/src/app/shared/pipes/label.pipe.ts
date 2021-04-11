import { Pipe, PipeTransform } from '@angular/core';
import {Concept} from "../model/concept.class";
import {Label} from "../model/label.class";

@Pipe({
  name: 'label'
})
export class LabelPipe implements PipeTransform {
  language: string = 'de';

  transform(value: Concept): unknown {
    let label: Label | undefined;
    if (!Array.isArray(value.labels)
        || value.labels.length === 0
        || (label = value.labels.find(l => l.language === this.language)) == null) {
      return value.id;
    }
    return label.text;
  }
}
