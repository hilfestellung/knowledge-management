import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {ConceptRoutingModule} from './concept-routing.module';
import {ConceptComponent} from './concept.component';
import {SharedModule} from "../../shared/shared.module";
import {MatListModule} from "@angular/material/list";
import {MatIconModule} from "@angular/material/icon";
import {MatButtonModule} from "@angular/material/button";
import {FlexLayoutModule} from "@angular/flex-layout";
import { ConceptItemComponent } from './components/concept-item/concept-item.component';


@NgModule({
  declarations: [ConceptComponent, ConceptItemComponent],
  imports: [
    CommonModule,
    ConceptRoutingModule,
    SharedModule,
    MatListModule,
    MatIconModule,
    MatButtonModule,
    FlexLayoutModule
  ],
  providers: []
})
export class ConceptModule {
}
