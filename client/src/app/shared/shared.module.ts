import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {ConceptService} from "./services/concept.service";
import { LabelPipe } from './pipes/label.pipe';
import {HttpClientModule} from "@angular/common/http";


@NgModule({
  declarations: [LabelPipe],
  imports: [
    CommonModule,
    HttpClientModule
  ],
  exports: [
    LabelPipe
  ],
  providers: [
    ConceptService
  ]
})
export class SharedModule {
}
