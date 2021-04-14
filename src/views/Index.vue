<template>
  <div class="logo">
      <div class="center-input">
        <h1 style="font-size: 70px;">nlutils</h1>
        <input type="text" name="keyword" class="search"/>
        <button class="search-button">Search</button>
      </div>
  </div>
</template>

<script>
export default {
    name: "Index"
}
</script>

<style lang="less" scoped>
.logo {
    position: absolute;
    top: 40%;
    left: 50%;
    transform: translate(-50%,-50%);
}

.search {
    margin-top: 2vh;
    border: 1px solid #000;
    width: 30vw;
    height: 3vh;
    font-size: 21px;
    border-radius: 4px;
    font-weight: bold;
}

.search-button {
    display: block;
    margin-top: 3vh;
    width: 10vw;
    height: 4vh;
    font-size: 20px;
    font-weight: bold;
    border-radius: 6px;
    background-color: transparent;
    color: rgb(37, 79, 195);
}

.center-input {
    width: 100%;
    height: 80vh;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}
</style>