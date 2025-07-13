import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ResponseForm } from './response-form';

describe('ResponseForm', () => {
  let component: ResponseForm;
  let fixture: ComponentFixture<ResponseForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ResponseForm]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ResponseForm);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
