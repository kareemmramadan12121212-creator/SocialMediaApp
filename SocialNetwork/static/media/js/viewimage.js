document.querySelector('.profile.image img').onclick = () => {
    document.querySelector('.imageview').style.display='flex'
}
document.querySelector('i.fa-regular.fa-circle-xmark').onclick = () => {
    document.querySelector('.imageview').style.display='none'
}