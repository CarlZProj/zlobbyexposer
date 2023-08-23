import React from "react";

import { HomePageWrapper, Img } from "./styles";

const summonersRiftImage = new URL(
	"../../assets/summoners_rift.jpg",
	import.meta.url
).href;

const HomePage = () => {
	return (
		<HomePageWrapper>
			<Img src={summonersRiftImage} alt="summoner's rift" />
		</HomePageWrapper>
	);
};

export default HomePage;
