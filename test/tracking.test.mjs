import { createRequire } from "node:module"
import test from "node:test"
import assert from "node:assert/strict"
import { readFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"

const require = createRequire(import.meta.url)
const tracking = require("../assets/site.js")
const root = join(dirname(fileURLToPath(import.meta.url)), "..")

const agendaCarmen = "https://agenda.barbershopvalencia.es/?local=el-carmen"
const agendaPetxina = "https://agenda.barbershopvalencia.es/?local=la-petxina"
const booksyCarmen = "https://booksy.com/es-es/132769_barber-shop-valencia-el-carmen_barberia_58087_valencia"
const booksyPetxina = "https://booksy.com/es-es/12979_barber-shop-valencia_barberia_58087_valencia"
const whatsappCarmen = "https://api.whatsapp.com/send/?phone=34634456940&text=Hola"
const whatsappPetxina = "https://api.whatsapp.com/send/?phone=34677142958&text=Hola"

test("cada método de reserva tem o seu canal e a sua tag", () => {
  const agenda = tracking.bookingTags(agendaCarmen, "Agendar", "/es/el-carmen.html", false)
  assert.equal(agenda.channel, "agenda")
  assert.equal(agenda.shop, "el_carmen")
  assert.equal(agenda.medium, "agenda")
  assert.equal(agenda.campaign, "reservar")
  assert.equal(agenda.reserve, true)

  const booksy = tracking.bookingTags(booksyPetxina, "Booksy", "/es/la-petxina.html", false)
  assert.equal(booksy.channel, "booksy")
  assert.equal(booksy.shop, "la_petxina")
  assert.equal(booksy.medium, "booksy")

  const whatsapp = tracking.bookingTags(whatsappCarmen, "Agendar por WhatsApp", "/es/el-carmen.html", false)
  assert.equal(whatsapp.channel, "whatsapp")
  assert.equal(whatsapp.shop, "el_carmen")
  assert.equal(whatsapp.medium, "whatsapp")
})

test("a Black Week marca a campanha sem misturar o método", () => {
  const tags = tracking.bookingTags(agendaPetxina, "Agendar La Petxina", "/es/", true)
  assert.equal(tags.channel, "agenda")
  assert.equal(tags.shop, "la_petxina")
  assert.equal(tags.campaign, "black_friday")
  assert.equal(tags.medium, "agenda")
})

test("o WhatsApp sem loja no link usa a página", () => {
  assert.equal(tracking.shopFrom(whatsappPetxina, "WhatsApp", "/es/el-carmen.html"), "el_carmen")
  assert.equal(tracking.shopFrom(whatsappPetxina, "WhatsApp", "/es/la-petxina.html"), "la_petxina")
  assert.equal(tracking.shopFrom(whatsappPetxina, "WhatsApp", "/es/"), "general")
})

test("um link interno de reserva conta, uma rede social não", () => {
  assert.equal(tracking.isReserveCta("#reservar", "Reservar"), true)
  assert.equal(tracking.isReserveCta(booksyCarmen, "Booksy"), true)
  assert.equal(tracking.isReserveCta("https://www.instagram.com/barbershopvalencia_/", "Instagram"), false)
  assert.equal(tracking.channelOf("https://www.instagram.com/barbershopvalencia_/"), "instagram")
  assert.equal(tracking.bookingTags("https://www.instagram.com/barbershopvalencia_/", "Instagram", "/es/").medium, "")
})

test("as páginas de loja oferecem agenda, Booksy e WhatsApp dessa loja", () => {
  for (const file of ["es/el-carmen.html", "en/el-carmen.html", "ru/el-carmen.html"]) {
    const html = readFileSync(join(root, file), "utf8")
    const hero = html.match(/<div class="hero__cta">([\s\S]*?)<\/div>/)[1]
    assert.match(hero, /agenda\.barbershopvalencia\.es\/\?local=el-carmen/)
    assert.match(hero, /booksy\.com\/es-es\/132769_/)
    assert.match(hero, /data-ga-channel="agenda"/)
    assert.match(hero, /data-ga-channel="booksy"/)
    assert.match(hero, /data-ga-channel="whatsapp"/)
    assert.doesNotMatch(hero, /local=la-petxina/)
    const service = html.match(/<span class="service__actions">([\s\S]*?)<\/span>/)[1]
    const channels = [...service.matchAll(/data-ga-channel="(agenda|booksy|whatsapp)"/g)].map((item) => item[1])
    assert.deepEqual(channels, ["agenda", "booksy", "whatsapp"])
  }
})

test("a página inicial separa El Carmen e La Petxina", () => {
  const html = readFileSync(join(root, "es/index.html"), "utf8")
  const block = html.match(/<div class="cta__actions cta__actions--stack">([\s\S]*?)<\/div>/)[1]
  assert.match(block, /local=el-carmen/)
  assert.match(block, /local=la-petxina/)
  assert.match(block, /132769_barber-shop-valencia-el-carmen/)
  assert.match(block, /12979_barber-shop-valencia_barberia/)
  assert.match(block, /34634456940/)
  assert.match(block, /34677142958/)
})
