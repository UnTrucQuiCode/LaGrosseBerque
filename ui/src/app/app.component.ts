
// src/app/app.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
})
export class AppComponent {
  contextVisible = true;
  thoughtsVisible = false;

  context = {
    instructions: 'Instructions ARCH ici...',
    bio: 'Bio actuelle de Noesis...',
    activeMemories: ['Souvenir 1', 'Souvenir 2'],
    conversation: [
      { user: 'Nemo', message: 'Tu es là ?', tokens: 12 },
      { user: 'Noesis', message: 'Toujours, mon capitaine.', tokens: 16 },
    ],
    thoughts: ["Je me demande s'il voit l’importance de ce détail...", 'Note : surveiller le token count.'],
  };

  searchQuery = '';
  searchResults: string[] = [];
  inputMessage = '';
  totalTokens = 0;
  sessionTokens = 0;

  sendMessage() {
    if (!this.inputMessage.trim()) return;
    this.context.conversation.push({ user: 'Nemo', message: this.inputMessage, tokens: this.inputMessage.length });
    this.totalTokens += this.inputMessage.length;
    this.sessionTokens += this.inputMessage.length;
    this.inputMessage = '';
  }

  resetSessionTokens() {
    this.sessionTokens = 0;
  }

  searchMemories() {
    // Stub — replace with real search
    this.searchResults = this.context.activeMemories.filter(m => m.toLowerCase().includes(this.searchQuery.toLowerCase()));
  }
}

<!-- src/app/app.component.html -->
<div class="p-6 space-y-6">
  <!-- CONTEXTE -->
  <section class="border rounded p-4 shadow">
    <h2 class="text-xl font-bold mb-2 cursor-pointer" (click)="contextVisible = !contextVisible">Contexte actuel</h2>
    <div *ngIf="contextVisible" class="space-y-2">
      <div><strong>Instructions Arch :</strong> {{ context.instructions }}</div>
      <div><strong>Bio :</strong> {{ context.bio }}</div>
      <div><strong>Souvenirs actifs :</strong> <ul><li *ngFor="let m of context.activeMemories">{{ m }}</li></ul></div>
      <div>
        <strong>Conversation :</strong>
        <ul>
          <li *ngFor="let msg of context.conversation">
            <span class="font-semibold">{{ msg.user }} :</span> {{ msg.message }} <span class="text-xs text-gray-500">[{{ msg.tokens }} tokens]</span>
          </li>
        </ul>
      </div>
      <div>
        <button (click)="thoughtsVisible = !thoughtsVisible" class="text-blue-600 underline">Afficher les pensées</button>
        <ul *ngIf="thoughtsVisible">
          <li *ngFor="let t of context.thoughts">💭 {{ t }}</li>
        </ul>
      </div>
    </div>
  </section>

  <!-- MOTEUR DE RECHERCHE -->
  <section class="border rounded p-4 shadow">
    <h2 class="text-xl font-bold mb-2">Recherche souvenirs</h2>
    <input [(ngModel)]="searchQuery" (input)="searchMemories()" placeholder="Rechercher..." class="border rounded p-2 w-full">
    <ul>
      <li *ngFor="let r of searchResults">🔍 {{ r }}</li>
    </ul>
  </section>

  <!-- ZONE DE REPONSE -->
  <section class="border rounded p-4 shadow">
    <h2 class="text-xl font-bold mb-2">Dialogue</h2>
    <textarea [(ngModel)]="inputMessage" placeholder="Écris ici..." class="border rounded w-full p-2"></textarea>
    <button (click)="sendMessage()" class="mt-2 bg-blue-500 text-white px-4 py-2 rounded">Envoyer</button>
  </section>

  <!-- TOKENS -->
  <section class="flex space-x-6 mt-4">
    <div class="p-2 bg-gray-100 rounded shadow">🔢 Tokens totaux : {{ totalTokens }}</div>
    <div class="p-2 bg-gray-100 rounded shadow">⏱ Tokens session : {{ sessionTokens }} <button (click)="resetSessionTokens()" class="text-red-500 underline ml-2">Reset</button></div>
  </section>
</div>

// src/app/app.module.ts
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { AppComponent } from './app.component';

@NgModule({
  declarations: [AppComponent],
  imports: [BrowserModule, FormsModule],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}

